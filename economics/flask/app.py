from flask import Flask, render_template, request, jsonify, render_template_string
import pymysql

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host="74.63.247.122",
        database="Stocks",
        user="remote_user",
        password="stocks123",
        port=3307
    )

# Route to render the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch unique symbols for dropdown filter
    cursor.execute("SELECT DISTINCT Symbol FROM Stocks")
    unique_symbols = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return render_template('index.html', unique_symbols=unique_symbols)

# Route to handle the table update via AJAX
@app.route('/filter-table', methods=['POST'])
def filter_table():
    page = request.json.get('page', 1)
    limit = 20
    offset = (page - 1) * limit
    symbol_filter = request.json.get('symbol')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    sort_order = request.json.get('sort_order', 'asc')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Build and execute query for table data
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

    cursor.close()
    connection.close()

    # Render table rows as HTML
    table_html = render_template_string("""
        <table>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Open</th>
                <th>High</th>
                <th>Low</th>
                <th>Close</th>
                <th>Volume</th>
                <th>Adj Close</th>
                <th>Symbol</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
                <td>{{ row[6] }}</td>
                <td>{{ row[7] }}</td>
                <td>{{ row[8] }}</td>
            </tr>
            {% endfor %}
        </table>
        <div class="pagination">
            {% if page > 1 %}
            <a href="#" onclick="loadTableData({{ page - 1 }})">Previous</a>
            {% endif %}
            {% if (page * limit) < total_rows %}
            <a href="#" onclick="loadTableData({{ page + 1 }})">Next</a>
            {% endif %}
        </div>
    """, rows=rows, page=page, limit=limit, total_rows=total_rows)

    return jsonify({'table_html': table_html})

# New route to fetch graph data via AJAX
@app.route('/get-graph-data', methods=['POST'])
def get_graph_data():
    selected_stocks = request.json.get('selected_stocks')
    y_column = request.json.get('y_column')

    connection = get_db_connection()
    cursor = connection.cursor()

    graph_data = {}
    if y_column and selected_stocks:
        for stock in selected_stocks:
            graph_query = f"SELECT Date, {y_column} FROM Stocks WHERE Symbol = %s"
            cursor.execute(graph_query, (stock,))
            graph_data[stock] = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(graph_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
