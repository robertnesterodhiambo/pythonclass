from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import joblib
import re
from werkzeug.security import generate_password_hash, check_password_hash
from math import ceil
import pandas as pd

# Load ML model
model = joblib.load("house_price_model.pkl")

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_CONFIG = {
    "host": "104.238.220.190",
    "user": "cashprohomebuyer_new_real_state",
    "password": "KH8lhGoLK4Sl",
    "database": "cashprohomebuyer_new_real_state"
}

# ✅ Ensure users table exists
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS C9HLVaiEgVWu_User (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            user_type ENUM('buyer', 'seller') NOT NULL,
            property_address VARCHAR(255),
            beds INT,
            baths INT,
            sqft INT,
            lot_size INT,
            year_built INT,
            county VARCHAR(100),
            estimated_value DECIMAL(15,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# ----------------- ROUTES ------------------

@app.route("/")
def index():
    return render_template("index.html")

# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user_type = request.form["user_type"]
        address = request.form["address"]
        beds = request.form["beds"]
        baths = request.form["baths"]
        sqft = request.form["sqft"]
        lot_size = request.form["lot_size"]
        year_built = request.form["year_built"]
        county = request.form["county"]

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.", "danger")
            return redirect(url_for("signup"))

        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Check uniqueness
        cur.execute("SELECT id FROM C9HLVaiEgVWu_User WHERE email=%s OR username=%s", (email, username))
        if cur.fetchone():
            flash("Email or username already exists!", "danger")
            conn.close()
            return redirect(url_for("signup"))

        # Predict house value
        try:
            features = [[int(beds), int(baths), int(sqft), int(lot_size), int(year_built)]]
            predicted_value = float(model.predict(features)[0])
        except Exception:
            predicted_value = None

        password_hash = generate_password_hash(password)

        cur.execute("""
            INSERT INTO C9HLVaiEgVWu_User 
            (username, email, password_hash, user_type, property_address, beds, baths, sqft, lot_size, year_built, county, estimated_value) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (username, email, password_hash, user_type, address, beds, baths, sqft, lot_size, year_built, county, predicted_value))

        conn.commit()
        conn.close()

        flash("Signup successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM C9HLVaiEgVWu_User WHERE email=%s", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["user_type"] = user["user_type"]
            session["is_admin"] = bool(user.get("is_admin", 0))

            return redirect(url_for("profile"))
        else:
            flash("Invalid login credentials", "danger")

    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM C9HLVaiEgVWu_User WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()
    conn.close()

    return render_template("profile.html", user=user)

# ---------- PROPERTIES PAGE ----------
@app.route("/properties/<state>")
def properties(state):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # map state to correct table
    if state.lower() == "ga":
        table = "propstream_ga"
    elif state.lower() == "nc":
        table = "propstream_nc"
    else:
        flash("Invalid state selection", "danger")
        return redirect(url_for("index"))

    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)

    cur.execute(f"SELECT COUNT(*) as total FROM {table}")
    total_rows = cur.fetchone()["total"]
    total_pages = ceil(total_rows / per_page)

    cur.execute(f"""
        SELECT address_db, beds, baths, sqFt, lot_size, status, county, estimated_value
        FROM {table}
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    rows = cur.fetchall()

    conn.close()

    # --- helper to parse city & zip from address_db ---
    def parse_city_zip(address):
        try:
            parts = [p.strip() for p in address.split(",")]
            city = parts[-2] if len(parts) >= 2 else ""
            zip_match = re.search(r"\b\d{5}\b", address)
            zip_code = zip_match.group(0) if zip_match else ""
            return city, zip_code
        except Exception:
            return "", ""

    # Predict estimated values using model’s expected input
    for r in rows:
        city, zip_code = parse_city_zip(r.get("address_db", ""))

        user_data = {
            "bed": int(r.get("beds") or 0),
            "bath": int(r.get("baths") or 0),
            "house_size": float(r.get("sqFt") or 0),
            "acre_lot": float(r.get("lot_size") or 0),
            "city": city,
            "state": state.upper(),
            "zip_code": zip_code,
            "status": str(r.get("status") or "Unknown"),
        }

        try:
            sample = pd.DataFrame([user_data])
            r["predicted_value"] = float(model.predict(sample)[0])
        except Exception:
            r["predicted_value"] = None

    return render_template("properties.html",
                           rows=rows,
                           state=state.upper(),
                           page=page,
                           total_pages=total_pages)

# ---------- ESTIMATE ----------
@app.route("/estimate", methods=["GET", "POST"])
def estimate():
    if "user_id" not in session:
        return redirect(url_for("login"))

    price = None
    user = None

    # fetch logged-in user (to show stored property)
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM C9HLVaiEgVWu_User WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()
    conn.close()

    if request.method == "POST":
        # get form input
        user_data = {
            "bed": int(request.form.get("bed", 0)),
            "bath": int(request.form.get("bath", 0)),
            "house_size": float(request.form.get("house_size", 0)),
            "acre_lot": float(request.form.get("acre_lot", 0)),
            "city": request.form.get("city", "Unknown"),
            "state": request.form.get("state", "Unknown"),
            "zip_code": request.form.get("zip_code", "00000"),
            "status": request.form.get("status", "Unknown"),
        }
        sample = pd.DataFrame([user_data])
        price = float(model.predict(sample)[0])

    return render_template("estimate.html", price=price, user=user)


@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or not session.get("is_admin"):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("index"))

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT id, username, email, user_type, property_address, beds, baths, sqft, lot_size, year_built, county, estimated_value, created_at
        FROM C9HLVaiEgVWu_User
        ORDER BY created_at DESC
    """)
    users = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", users=users)



# ----------------- RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)
