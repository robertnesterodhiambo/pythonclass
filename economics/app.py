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
    symbol_filter = request.form.get('symbol')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    sort_order = request.form.get('sort_order', 'asc')
    y_column = request.form.get('y_column')
    selected_stocks = request.form.getlist('selected_stocks')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
        unique_symbols = [row[0] for row in cursor.fetchall()]

        # Build the query with filtering and sorting
        query = "SELECT * FROM Stocks"
        conditions = []
        if symbol_filter:
            conditions.append(f"Symbol = '{symbol_filter}'")
        if start_date:
            conditions.append(f"Date >= '{start_date}'")
        if end_date:
            conditions.append(f"Date <= '{end_date}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += f" ORDER BY Date {'ASC' if sort_order == 'asc' else 'DESC'} LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))

        rows = cursor.fetchall()

        # Fetch total rows for pagination
        cursor.execute("SELECT COUNT(*) FROM Stocks")
        total_rows = cursor.fetchone()[0]

        # Fetch data for graphing
        graph_data = {}
        if y_column and selected_stocks:
            for stock in selected_stocks:
                graph_query = f"SELECT Date, {y_column} FROM Stocks WHERE Symbol = %s"
                cursor.execute(graph_query, (stock,))
                graph_data[stock] = cursor.fetchall()

        return render_template('index.html', rows=rows, page=page, total_rows=total_rows, limit=limit, 
                               unique_symbols=unique_symbols, selected_symbol=symbol_filter, 
                               sort_order=sort_order, start_date=start_date, end_date=end_date,
                               y_column=y_column, graph_data=graph_data, selected_stocks=selected_stocks)

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
    app.run(debug=True,host='0.0.0.0',port=5001)
