import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# === 1. Load data ===
df = pd.read_csv("realtor-data.zip.csv")

# === 2. Preprocessing ===
df = df.dropna(subset=["price"])

df["prev_sold_date"] = pd.to_datetime(df["prev_sold_date"], errors="coerce")
df["sold_year"] = df["prev_sold_date"].dt.year.fillna(0)

# === 3. Select features ===
target = "price"
features = ['bed', 'bath', 'acre_lot', 'house_size', 'city', 'state', 'zip_code', 'brokered_by', 'status', 'sold_year']
X = df[features].copy()
y = df[target]

# === 4. Handle missing numerics ===
for col in ['acre_lot', 'house_size', 'bed', 'bath']:
    X[col] = X[col].fillna(X[col].median())

# === 5. Define encoders ===
categorical_cols = ['city', 'state', 'zip_code', 'brokered_by', 'status']
numeric_cols = ['bed', 'bath', 'acre_lot', 'house_size', 'sold_year']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), categorical_cols)
    ],
    remainder='passthrough'
)

# === 6. Model pipeline ===
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42))
])

# === 7. Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 8. Train ===
model.fit(X_train, y_train)

# === 9. Predict & evaluate ===
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"✅ RMSE: ${rmse:,.2f}")
print(f"✅ R² Score: {r2:.4f}")

import joblib

# Save the full pipeline (preprocessing + model)
joblib.dump(model, "house_price_model.pkl")

print("✅ Model saved as house_price_model.pkl")