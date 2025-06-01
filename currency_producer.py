from kafka import KafkaProducer
import json, random, time
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("📡 Kafka Producer z pełnym snapshotem – START")

waluty = ("EUR", "USD", "GBP")
endDate = datetime.today().date()
startDate = endDate - relativedelta(years=1)

# --- Pobieranie danych z NBP ---
kurs_walut = pd.DataFrame()

for kod in waluty:
    url = f'https://api.nbp.pl/api/exchangerates/rates/c/{kod}/{startDate}/{endDate}/?format=json'
    response = requests.get(url)
    dane_json = response.json()
    dane = pd.DataFrame(dane_json["rates"])[["effectiveDate", "bid", "ask"]]
    dane.rename(columns={"bid": f"{kod}_bid", "ask": f"{kod}_ask"}, inplace=True)
    dane["effectiveDate"] = pd.to_datetime(dane["effectiveDate"])
    kurs_walut = dane if kurs_walut.empty else pd.merge(kurs_walut, dane, on="effectiveDate", how="outer")

# --- Statystyki bazowe do generowania syntetycznych kursów ---
pods_waluty = {}
for kol in kurs_walut.columns[1:]:
    mean = kurs_walut[kol].mean()
    var = kurs_walut[kol].var()
    last = kurs_walut.loc[kurs_walut['effectiveDate'].idxmax(), kol]
    pods_waluty[kol] = (last, mean, var)

# --- Funkcja generująca jeden snapshot kursów ---
def generuj_snapshot_kursow():
    snapshot = {"timestamp": datetime.utcnow().isoformat()}
    for waluta in waluty:
        for typ in ["bid", "ask"]:
            key = f"{waluta}_{typ}"
            z, x, y = pods_waluty[key]
            zmiana = random.choice([-1, 1])
            zmiennosc = np.random.normal(loc=x, scale=np.sqrt(y))
            nowy_kurs = round(z + zmiana * 0.001 * zmiennosc, 5)
            pods_waluty[key] = (nowy_kurs, x, y)
            snapshot[key] = nowy_kurs
    return snapshot

# --- Główna pętla: co 2 sekundy wysyła pełny snapshot ---
while True:
    snapshot = generuj_snapshot_kursow()
    producer.send("kursy-walut", value=snapshot)
    print(f"📤 Kafka snapshot wysłany: {snapshot}")
    time.sleep(2)
