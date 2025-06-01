# Analiza danych kursów walutowych w czasie rzeczywistym

Projekt oparty na przetwarzaniu strumieniowym danych walutowych w czasie rzeczywistym oraz podejmowaniu decyzji inwestycyjnych z użyciem modelu uczenia maszynowego.

---

## 🎯 Cel projektu

Celem projektu było stworzenie systemu symulującego działanie prostego agenta inwestycyjnego, który na podstawie aktualnych kursów walut podejmuje decyzje o najkorzystniejszej wymianie jednej waluty na inną, maksymalizując wartość portfela wyrażoną w PLN.

---

## ⚙️ Technologie

- **Python**
- **Apache Kafka (Docker)**
- **XGBoost (ML)**
- **Pandas / NumPy / Matplotlib**
- **NBP API (dane historyczne kursów walut)**

---

## 📈 Opis działania

1. **Generowanie danych**  
   Dane kursowe dla EUR, USD, GBP względem PLN zostały pobrane z API NBP, następnie użyto ich do wygenerowania syntetycznego zbioru danych kursowych w formie strumienia (co 2 sekundy).

2. **Tworzenie etykiet**  
   Każdemu snapshotowi danych przypisano etykietę odpowiadającą najkorzystniejszej wymianie waluty, spośród możliwych klas (np. EUR→USD, PLN→GBP itd.).

3. **Trenowanie modelu**  
   - Model klasyfikacyjny XGBoost został wytrenowany na ok. 30 000 obserwacjach.
   - Dane były zrównoważone za pomocą metody **SMOTE**, aby uniknąć przewagi częstych klas.
   - Etykieta (`label`) wskazuje optymalną decyzję inwestycyjną w krótkim horyzoncie czasowym.

4. **Streaming i podejmowanie decyzji**  
   - Producent Kafka generuje dane kursowe i przesyła je co 2 sekundy do topiku.
   - Konsument odbiera dane, przelicza wszystkie kursy par walutowych i na ich podstawie model wskazuje najlepszą wymianę.
   - Co trzecią decyzję model losuje akcję, by symulować ograniczoną pewność.
   - Portfel aktualizuje się w czasie rzeczywistym, a historia decyzji zapisywana jest do pliku CSV.

5. **Wizualizacja wyników**  
   - Wykres zmian wartości portfela w czasie.
   - Wykresy przedstawiające zmiany stanu poszczególnych walut.

---

## 🧠 Możliwe ulepszenia

- Użycie **realnych danych sekundowych** z dłuższego okresu.
- Wprowadzenie klasy „hold” – brak działania w danym momencie.
- Umożliwienie **wielu transakcji jednocześnie** (np. wymiana różnych walut za różne kwoty).
- Zniesienie sztywnego limitu 100 jednostek na transakcję.
- Zastosowanie bardziej zaawansowanych modeli ML (np. LSTM, reinforcement learning).
- Ulepszenie strategii decyzyjnej poprzez analizę trendów lub zmienności rynku.

---

## 🚀 Uruchomienie

1. Uruchom środowisko Kafka (np. z Docker Compose).
2. W terminalu uruchom producenta danych:
   ```bash
   python currency_producer.py
3. W drugim terminalu uruchom konsumenta:
   ```bash
   python currency_consumer.py`
4. Po zakończeniu symulacji wygeneruj wykresy:
   ```bash
   wizualizacja_wynikow.py'

