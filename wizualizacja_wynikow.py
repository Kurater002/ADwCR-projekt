import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("history.csv", parse_dates=["timestamp"])


# Wykres - Zmiana wartości portfela w czasie
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["wartosc_portfela"], label="Wartość portfela (PLN)")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.xlabel("Czas (godzina)")
plt.ylabel("Wartość portfela (PLN)")
plt.title("Zmiana wartości portfela w czasie")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Wykres - Zmiana każdej waluty w portfelu w czasie
plt.figure(figsize=(12, 6))
for waluta in ["PLN", "USD", "EUR", "GBP"]:
    plt.plot(df["timestamp"], df[waluta], label=waluta)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.xlabel("Czas (godzina)")
plt.ylabel("Ilość waluty")
plt.title("Zmiana stanu każdej waluty w portfelu w czasie")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.gcf().autofmt_xdate()  # (opcjonalnie) obraca etykiety X jeśli są gęsto
plt.show()


# Wynik finansowy
def pokaz_podsumowanie_z_csv(history_file="history.csv"):
    df = pd.read_csv(history_file)
    if df.empty:
        print("📭 Brak danych w pliku historii.")
        return

    wartosc_startowa = df["wartosc_portfela"].iloc[0]
    wartosc_koncowa = df["wartosc_portfela"].iloc[-1]
    roznica = wartosc_koncowa - wartosc_startowa

    print("\n📊 Podsumowanie symulacji:")
    print(f"💼 Wartość początkowa portfela: {wartosc_startowa:.2f} PLN")
    print(f"💼 Wartość końcowa portfela:   {wartosc_koncowa:.2f} PLN")
    print(f"📈 Zysk/strata: {roznica:+.2f} PLN")

# Użycie:
pokaz_podsumowanie_z_csv("history.csv")

