import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ================================
# 1. Load Data
# ================================
df = pd.read_csv("realtor-data.zip.csv")

# Keep only relevant columns
features = [
    "bed", "bath", "house_size", "acre_lot",
    "city", "state", "zip_code", "status"
]
target = "price"

# Drop rows without target
df = df.dropna(subset=[target])

X = df[features]
y = df[target]

# ================================
# 2. Handle Missing Values
# ================================
X = X.fillna({
    "bed": 0,
    "bath": 0,
    "house_size": X["house_size"].median(),
    "acre_lot": X["acre_lot"].median(),
    "city": "Unknown",
    "state": "Unknown",
    "zip_code": "00000",
    "status": "Unknown"
})

# Force categorical features into strings
categorical_features = ["city", "state", "zip_code", "status"]
for col in categorical_features:
    X[col] = X[col].astype(str)

# ================================
# 3. Preprocessing
# ================================
numeric_features = ["bed", "bath", "house_size", "acre_lot"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# ================================
# 4. Model Pipeline
# ================================
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
])

# ================================
# 5. Train/Test Split
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

# ================================
# 6. Save Model
# ================================
joblib.dump(model, "house_price_model.pkl")
print("✅ Model saved as house_price_model.pkl")

# ================================
# 7. Take User Input for Prediction
# ================================
loaded_model = joblib.load("house_price_model.pkl")

print("\nEnter property details for prediction:")

user_data = {
    "bed": int(input("Bedrooms: ")),
    "bath": int(input("Bathrooms: ")),
    "house_size": float(input("House size (sqft): ")),
    "acre_lot": float(input("Lot size (acres): ")),
    "city": input("City: "),
    "state": input("State: "),
    "zip_code": input("Zip code: "),
    "status": input("Status (for_sale/sold/pending): ")
}

sample = pd.DataFrame([user_data])
predicted_price = loaded_model.predict(sample)[0]
print(f"\n💰 Predicted Price: ${predicted_price:,.2f}")
