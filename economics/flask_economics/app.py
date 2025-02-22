from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_stock_data(page, per_page=50):
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
    cursor.execute("SELECT * FROM Stocks LIMIT %s OFFSET %s", (per_page, offset))
    columns = [col[0] for col in cursor.description]  # Fetch column names
    data = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM Stocks")
    total_rows = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    total_pages = (total_rows + per_page - 1) // per_page
    return columns, data, total_pages

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    columns, stock_data, total_pages = get_stock_data(page)
    return render_template('index.html', columns=columns, stock_data=stock_data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
