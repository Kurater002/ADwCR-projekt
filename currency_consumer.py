from kafka import KafkaConsumer
import json
import joblib
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
import random
import csv
import os

model = joblib.load("model_xgb_multi_currency.pkl")
label_encoder = joblib.load("label_encoder.pkl")
all_labels = list(label_encoder.classes_)

# Konsument Kafka
consumer = KafkaConsumer(
    'kursy-walut',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

# Portfel początkowy
waluty = ['PLN', 'USD', 'EUR', 'GBP']
portfel = {waluta: 10000.0 for waluta in waluty}
predykcji_licznik = 0

# Plik do zapisania historii
historia_file = "history.csv"
if not os.path.exists(historia_file):
    with open(historia_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "akcja", "PLN", "USD", "EUR", "GBP", "wartosc_portfela"])

print("🔁 Start konsumenta i symulacji...")

for msg in consumer:
    dane = msg.value

    if not all(f"{w}_bid" in dane and f"{w}_ask" in dane for w in ['UiSD', 'EUR', 'GBP']):
        continue

    # Kursy wymiany
    features = {
        'PLN_USD': 1 / dane['USD_ask'],
        'USD_PLN': dane['USD_bid'],
        'PLN_EUR': 1 / dane['EUR_ask'],
        'EUR_PLN': dane['EUR_bid'],
        'PLN_GBP': 1 / dane['GBP_ask'],
        'GBP_PLN': dane['GBP_bid'],
        'USD_EUR': dane['USD_bid'] / dane['EUR_ask'],
        'EUR_USD': dane['EUR_bid'] / dane['USD_ask'],
        'USD_GBP': dane['USD_bid'] / dane['GBP_ask'],
        'GBP_USD': dane['GBP_bid'] / dane['USD_ask'],
        'EUR_GBP': dane['EUR_bid'] / dane['GBP_ask'],
        'GBP_EUR': dane['GBP_bid'] / dane['EUR_ask'],
    }

    X = np.array([list(features.values())])

    predykcji_licznik += 1
    if predykcji_licznik >= 3:
        label = random.choice(all_labels)
        predykcji_licznik = 0
    else:
        label_encoded = model.predict(X)[0]
        label = label_encoder.inverse_transform([label_encoded])[0]

    if '→' in label:
        src, tgt = label.split('→')
        kwota = 100.0

        if portfel[src] >= kwota:
            rate = features[f"{src}_{tgt}"]
            zysk = kwota * rate
            portfel[src] -= kwota
            portfel[tgt] += zysk

            print(f"✅ {label}: {kwota:.2f} {src} → {zysk:.2f} {tgt} po kursie {rate:.4f}")
        else:
            print(f"❌ Brak środków w {src}, pomijam transakcję.")
            label = "brak"

    # Obliczenie wartości portfela w PLN
    wartosc = (
        portfel['PLN']
        + portfel['USD'] * dane['USD_bid']
        + portfel['EUR'] * dane['EUR_bid']
        + portfel['GBP'] * dane['GBP_bid']
    )

    print(f"💼 Portfel: " + " | ".join([f"{k}: {v:.2f}" for k, v in portfel.items()]))
    print(f"💰 Wartość portfela (PLN): {wartosc:.2f}\n")

    # Zapis wyników
    with open(historia_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            dane["timestamp"], label,
            portfel["PLN"], portfel["USD"], portfel["EUR"], portfel["GBP"],
            wartosc
        ])
