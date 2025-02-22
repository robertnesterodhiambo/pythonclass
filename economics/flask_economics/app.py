from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

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
    
    # Handle case where no data is returned
    if cursor.description:
        columns = [col[0] for col in cursor.description]  # Fetch column names
    else:
        columns = []
    
    if symbol_filter:
        cursor.execute("SELECT COUNT(*) FROM Stocks WHERE Symbol = %s", (symbol_filter,))
    else:
        cursor.execute("SELECT COUNT(*) FROM Stocks")
    
    total_rows = cursor.fetchone()[0] if cursor.rowcount > 0 else 0  # Ensure row count exists
    
    cursor.execute("SELECT DISTINCT Symbol FROM Stocks")  # Fetch distinct symbols for filtering
    symbols = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    total_pages = (total_rows + per_page - 1) // per_page if total_rows > 0 else 1
    return columns, data, total_pages, symbols

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    symbol_filter = request.args.get('symbol', None)
    columns, stock_data, total_pages, symbols = get_stock_data(page, symbol_filter)
    return render_template('index.html', columns=columns, stock_data=stock_data, page=page, total_pages=total_pages, symbols=symbols, selected_symbol=symbol_filter)

if __name__ == '__main__':
    app.run(debug=True)
