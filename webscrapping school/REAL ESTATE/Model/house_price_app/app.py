from flask import Flask, render_template, request
import joblib
import pandas as pd

# ===============================
# Load trained model
# ===============================
model = joblib.load("house_price_model.pkl")

app = Flask(__name__)

# ===============================
# Routes
# ===============================
@app.route("/")
def home():
    return render_template("index.html")  # form page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
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

        # Convert to DataFrame
        sample = pd.DataFrame([user_data])

        # Predict
        predicted_price = model.predict(sample)[0]

        return render_template(
            "result.html",
            price=f"${predicted_price:,.2f}"
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
