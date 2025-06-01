import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

# 1. Wczytaj dane
df = pd.read_csv("dane/labeled_currency_data_balanced.csv")

# 2. Przygotuj dane wejściowe
X = df.drop(columns=["label"])
y = df["label"]

# 3. Zakoduj etykiety
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 5. Parametry do GridSearch
param_grid = {
    "n_estimators": [50, 100, 150, 200],
    "max_depth": [3, 4, 5, 7],
    "learning_rate": [0.01, 0.05, 0.1],
}

# 6. Inicjalizacja modelu
xgb = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)

# 7. Grid Search
grid_search = GridSearchCV(xgb, param_grid, cv=3, verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 8. Najlepszy model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# 9. Ewaluacja
print("🎯 Najlepsze parametry:", grid_search.best_params_)
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("🎯 Raport klasyfikacji:\n", classification_report(y_test, y_pred, target_names=le.classes_))

# 10. Zapis modelu i encoderów
joblib.dump(best_model, "model_xgb_multi_currency.pkl")
joblib.dump(le, "label_encoder.pkl")
print("✅ Zapisano model i encoder.")
