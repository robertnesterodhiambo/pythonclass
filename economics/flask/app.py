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

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    symbol_filter = request.form.get('symbol')  # Get the selected symbol from the form

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch unique symbols for the dropdown
        cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
        unique_symbols = [row[0] for row in cursor.fetchall()]

        # Build the query with filtering
        if symbol_filter:
            cursor.execute("SELECT * FROM Stocks WHERE Symbol = %s LIMIT %s OFFSET %s", (symbol_filter, limit, offset))
        else:
            cursor.execute("SELECT * FROM Stocks LIMIT %s OFFSET %s", (limit, offset))

        rows = cursor.fetchall()

        # Get the total number of rows
        cursor.execute("SELECT COUNT(*) FROM Stocks")
        total_rows = cursor.fetchone()[0]

        return render_template('index.html', rows=rows, page=page, total_rows=total_rows, limit=limit, unique_symbols=unique_symbols, selected_symbol=symbol_filter)

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
