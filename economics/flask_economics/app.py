from flask import Flask, render_template, request, send_file, jsonify
import pymysql
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

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
        page=page,  # Pass page variable
        total_pages=total_pages,  # Pass total_pages
        symbols=symbols,  # Pass available symbols
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

if __name__ == '__main__':
    app.run(debug=True)
