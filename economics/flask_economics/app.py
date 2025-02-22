from flask import Flask, render_template, request, send_file, jsonify
import pymysql
import matplotlib.pyplot as plt
import io
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

MODEL_DIR = "~/Bob/Stock/stock_models"

# Function to fetch stock data with pagination
def get_stock_data(page, symbol_filter=None, per_page=50):
    conn = pymysql.connect(
        host="localhost",
        database="Stocks",
        user="root",
        password="1234",
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    
    if symbol_filter:
        cursor.execute("SELECT * FROM Stocks WHERE Symbol = %s LIMIT %s OFFSET %s", (symbol_filter, per_page, offset))
    else:
        cursor.execute("SELECT * FROM Stocks LIMIT %s OFFSET %s", (per_page, offset))
    
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description] if cursor.description else []
    
    if symbol_filter:
        cursor.execute("SELECT COUNT(*) FROM Stocks WHERE Symbol = %s", (symbol_filter,))
    else:
        cursor.execute("SELECT COUNT(*) FROM Stocks")
    
    total_rows = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
    
    cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
    symbols = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    total_pages = (total_rows + per_page - 1) // per_page if total_rows > 0 else 1
    return columns, data, total_pages, symbols

# Homepage with stock data table and filter
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    symbol_filter = request.args.get('symbol', None)
    columns, stock_data, total_pages, symbols = get_stock_data(page, symbol_filter)
    
    return render_template(
        'index.html',
        columns=columns,
        stock_data=stock_data,
        page=page,
        total_pages=total_pages,
        symbols=symbols,
        selected_symbol=symbol_filter
    )

# API to return stock data for chart plotting
@app.route('/plot')
def plot():
    symbol = request.args.get('symbol')
    column = request.args.get('column')

    if not symbol or column not in ['Open', 'High', 'Low', 'Close', 'Volume']:
        return jsonify({'error': 'Invalid symbol or column'}), 400
    
    conn = pymysql.connect(
        host="localhost",
        database="Stocks",
        user="root",
        password="1234",
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT Date, {column} FROM Stocks WHERE Symbol = %s ORDER BY Date", (symbol,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not data:
        return jsonify({'error': 'No data available'}), 404

    dates, values = zip(*data)
    
    return jsonify({'dates': dates, 'values': values})

# LSTM Stock Prediction API
@app.route('/predict')
def predict():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    model_path = os.path.join(MODEL_DIR, f"{symbol}.h5")
    if not os.path.exists(model_path):
        return jsonify({'error': 'Model not found for this symbol'}), 404
    
    conn = pymysql.connect(
        host="localhost",
        database="Stocks",
        user="root",
        password="1234",
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT Close FROM Stocks WHERE Symbol = %s ORDER BY Date DESC LIMIT 60", (symbol,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not data or len(data) < 60:
        return jsonify({'error': 'Not enough data for prediction'}), 400
    
    data = np.array([row[0] for row in reversed(data)]).reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    
    model = tf.keras.models.load_model(model_path)
    prediction = model.predict(np.expand_dims(scaled_data, axis=0))
    predicted_price = scaler.inverse_transform(prediction)[0][0]
    
    return jsonify({'symbol': symbol, 'predicted_price': predicted_price})

if __name__ == '__main__':
    app.run(debug=True)
