from flask import Flask, render_template, request, jsonify
import pymysql
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "Stocks",
    "user": "root",
    "password": "1234",
    "port": 3306,
    "charset": "utf8mb4",
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

    # Symbol filter
    selected_symbol = request.args.get('symbol', '')

    query = "SELECT Symbol, Open, High, Low, Close, Date FROM Stocks"
    params = []
    
    if selected_symbol:
        query += " WHERE Symbol = %s"
        params.append(selected_symbol)

    query += " ORDER BY Date DESC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    stock_data = cursor.fetchall()

    # Get total count for pagination
    count_query = "SELECT COUNT(*) FROM Stocks"
    count_params = []
    
    if selected_symbol:
        count_query += " WHERE Symbol = %s"
        count_params.append(selected_symbol)

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
        selected_symbol=selected_symbol
    )

@app.route('/get_stock_data')
def get_stock_data():
    symbol = request.args.get('symbol')
    column = request.args.get('column', 'Close')

    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    valid_columns = {"Open", "High", "Low", "Close"}
    if column not in valid_columns:
        return jsonify({'error': 'Invalid column'}), 400

    cursor.execute(f"SELECT Date, {column} FROM Stocks WHERE Symbol = %s ORDER BY Date ASC", (symbol,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    if not data:
        return jsonify({'error': 'No data found'}), 400

    dates = [str(row[0]) for row in data]
    values = [row[1] for row in data]

    return jsonify({'dates': dates, 'values': values})

@app.route('/predict')
def predict():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Close FROM Stocks WHERE Symbol = %s ORDER BY Date DESC LIMIT 60", (symbol,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    if not data or len(data) < 60:
        return jsonify({'error': 'Not enough data for prediction'}), 400

    prices = np.array([row[0] for row in reversed(data)]).reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_prices = scaler.fit_transform(prices)

    X_train = np.arange(len(scaled_prices)).reshape(-1, 1)
    y_train = scaled_prices
    model = LinearRegression()
    model.fit(X_train, y_train)

    next_day = np.array([[len(scaled_prices)]])
    scaled_prediction = model.predict(next_day)
    predicted_price = scaler.inverse_transform(scaled_prediction)[0][0]

    return jsonify({'symbol': symbol, 'predicted_price': round(predicted_price, 2)})

if __name__ == '__main__':
    app.run(debug=True)
