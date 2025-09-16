from flask import Flask, render_template, request
import joblib
import pandas as pd
import mysql.connector

# Load trained ML model
model = joblib.load("house_price_model.pkl")

# Flask app
app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="104.238.220.190",
        user="cashprohomebuyer_new_real_state",
        password="KH8lhGoLK4Sl",
        database="cashprohomebuyer_new_real_state"
    )

@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    state = None

    if request.method == "POST":
        state = request.form.get("state")

        if state == "ga":
            table = "propstream_ga"
        elif state == "nc":
            table = "propstream_nc"
        else:
            table = None

        if table:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(f"""
                SELECT ga_id, address_db, beds, baths, sqFt, lot_size, year_built,
                       property_type, status, county, estimated_value
                FROM {table} LIMIT 30
            """)
            rows = cursor.fetchall()

            conn.close()

            # Convert SQL data to DataFrame for prediction
            df = pd.DataFrame(rows)

            # Prepare features for model
            if not df.empty:
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

                # Add predictions to each row
                for i, row in enumerate(rows):
                    row["predicted_value"] = round(predictions[i], 2)

            data = rows

    return render_template("index.html", data=data, state=state)

if __name__ == "__main__":
    app.run(debug=True)
