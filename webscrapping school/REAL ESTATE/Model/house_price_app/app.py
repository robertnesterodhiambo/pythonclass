from flask import Flask, render_template, request
import joblib
import pandas as pd
import mysql.connector
import math

# Load trained ML model
model = joblib.load("house_price_model.pkl")

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="104.238.220.190",
        user="cashprohomebuyer_new_real_state",
        password="KH8lhGoLK4Sl",
        database="cashprohomebuyer_new_real_state"
    )

# ================================
# Home route: Select state & show paginated properties
# ================================
@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    state = None
    page = int(request.args.get("page", 1))
    per_page = 30
    total_pages = 1

    if request.method == "POST":
        state = request.form.get("state")
    else:
        state = request.args.get("state")

    if state in ["ga", "nc"]:
        table = f"propstream_{state}"

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Count total rows for pagination
        cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
        total_rows = cursor.fetchone()["cnt"]
        total_pages = math.ceil(total_rows / per_page)

        # Fetch paginated rows
        offset = (page - 1) * per_page
        cursor.execute(f"""
            SELECT ga_id, address_db, beds, baths, sqFt, lot_size, year_built,
                   property_type, status, county, estimated_value
            FROM {table} 
            LIMIT {per_page} OFFSET {offset}
        """)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            df = pd.DataFrame(rows)

            # Prepare features for ML model
            features = {
                "bed": df["beds"].fillna(0),
                "bath": df["baths"].fillna(0),
                "house_size": df["sqFt"].fillna(df["sqFt"].median()),
                "acre_lot": df["lot_size"].fillna(df["lot_size"].median()),
                "city": df["county"].fillna("Unknown"),
                "state": state.upper(),
                "zip_code": "00000",   # Placeholder
                "status": df["status"].fillna("Unknown")
            }
            feature_df = pd.DataFrame(features)

            predictions = model.predict(feature_df)

            # Attach predictions to rows
            for i, row in enumerate(rows):
                row["predicted_value"] = round(predictions[i], 2)

        data = rows

    return render_template("index.html", 
                           data=data, 
                           state=state, 
                           page=page, 
                           total_pages=total_pages)

# ================================
# User Input: Get House Price Estimate
# ================================
@app.route("/estimate", methods=["GET", "POST"])
def estimate():
    predicted_price = None

    if request.method == "POST":
        user_data = {
            "bed": int(request.form["bed"]),
            "bath": int(request.form["bath"]),
            "house_size": float(request.form["house_size"]),
            "acre_lot": float(request.form["acre_lot"]),
            "city": request.form["city"],
            "state": request.form["state"],
            "zip_code": request.form["zip_code"],
            "status": request.form["status"]
        }

        sample = pd.DataFrame([user_data])
        predicted_price = model.predict(sample)[0]

    return render_template("estimate.html", price=predicted_price)

if __name__ == "__main__":
    app.run(debug=True)
