from flask import Flask, render_template, request, jsonify
import pymysql
import numpy as np
import os
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
    
    # Fetch distinct stock symbols
    cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
    symbols = [row[0] for row in cursor.fetchall()]
    
    # Fetch stock data (latest 10 entries for simplicity)
    cursor.execute("SELECT Symbol, Open, High, Low, Close FROM Stocks ORDER BY Date DESC LIMIT 10")
    stock_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', symbols=symbols, stock_data=stock_data)

@app.route('/predict')
def predict():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch last 60 closing prices for the given stock
    cursor.execute("SELECT Close FROM Stocks WHERE Symbol = %s ORDER BY Date DESC LIMIT 60", (symbol,))
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if not data or len(data) < 60:
        return jsonify({'error': 'Not enough data for prediction'}), 400
    
    # Prepare the data
    prices = np.array([row[0] for row in reversed(data)]).reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_prices = scaler.fit_transform(prices)

    # Train a simple linear regression model as an alternative to LSTM
    X_train = np.arange(len(scaled_prices)).reshape(-1, 1)
    y_train = scaled_prices
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict the next day's price
    next_day = np.array([[len(scaled_prices)]])
    scaled_prediction = model.predict(next_day)
    predicted_price = scaler.inverse_transform(scaled_prediction)[0][0]

    return jsonify({'symbol': symbol, 'predicted_price': predicted_price})

if __name__ == '__main__':
    app.run(debug=True)
