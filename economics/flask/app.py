from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="74.63.247.122",
        database="Stocks",
        user="remote_user",
        password="stocks123",
        port=3307
    )

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # Get the current page number
    limit = 20
    offset = (page - 1) * limit

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute a query to fetch a limited number of rows
        cursor.execute("SELECT * FROM Stocks LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()

        # Get the total number of rows in the Stocks table
        cursor.execute("SELECT COUNT(*) FROM Stocks")
        total_rows = cursor.fetchone()[0]

        return render_template('index.html', rows=rows, page=page, total_rows=total_rows, limit=limit)

    except Exception as e:
        return f"Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/next')
def next_page():
    page = request.args.get('page', 1, type=int) + 1
    return index()

@app.route('/previous')
def previous_page():
    page = request.args.get('page', 1, type=int) - 1
    return index()

if __name__ == "__main__":
    app.run(debug=True)
