from flask import Flask, render_template, request, jsonify
import pymysql
import numpy as np

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
   # "host": "localhost",
   "host" : "104.238.220.190",
    "database": "stocksjbetadev_Stocks",
    "user": "stocksjbetadev",
    "password": "qZh]R0+inyo+",
   #"database": "Stocks",
   #"user": "root",
   #"password": "1234",
    "port": 3306,
    #"charset": "utf8mb4",
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch distinct stock symbols for filtering
    cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
    symbols = [row[0] for row in cursor.fetchall()]

    # Pagination setup
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Filters
    selected_symbol = request.args.get('symbol', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = "SELECT Symbol, Open, High, Low, Close, Date FROM Stocks WHERE 1=1"
    params = []
    
    if selected_symbol:
        query += " AND Symbol = %s"
        params.append(selected_symbol)
    
    if start_date:
        query += " AND Date >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND Date <= %s"
        params.append(end_date)

    query += " ORDER BY Date DESC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    stock_data = cursor.fetchall()

    # Get total count for pagination
    count_query = "SELECT COUNT(*) FROM Stocks WHERE 1=1"
    count_params = []
    
    if selected_symbol:
        count_query += " AND Symbol = %s"
        count_params.append(selected_symbol)
    
    if start_date:
        count_query += " AND Date >= %s"
        count_params.append(start_date)
    
    if end_date:
        count_query += " AND Date <= %s"
        count_params.append(end_date)

    cursor.execute(count_query, count_params)
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + per_page - 1) // per_page

    cursor.close()
    conn.close()

    return render_template(
        'index.html',
        symbols=symbols,
        stock_data=stock_data,
        page=page,
        total_pages=total_pages,
        selected_symbol=selected_symbol,
        start_date=start_date,
        end_date=end_date
    )

@app.route('/predict')
def predict():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Close FROM Stocks WHERE Symbol = %s ORDER BY Date DESC LIMIT 2", (symbol,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    if not data or len(data) < 2:
        return jsonify({'error': 'Not enough data for prediction'}), 400

    latest_price = float(data[0][0])
    previous_price = float(data[1][0])
    
    price_change = latest_price - previous_price
    predicted_price = latest_price + (0.15 * price_change)

    return jsonify({'predicted_price': predicted_price, 'symbol': symbol})

if __name__ == "__main__":
    app.run(debug=True)
