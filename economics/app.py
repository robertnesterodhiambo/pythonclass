import pymysql

def fetch_data():
    connection = None
    cursor = None

    try:
        # Connect to the remote MySQL database
        connection = pymysql.connect(
            host="74.63.247.122",  # Your remote database host
            database="Stocks",      # Your database name
            user="remote_user",     # Your username
            password="stocks123" ,   # Your password
            port = 3307
        )

        cursor = connection.cursor()

        # Execute a query to fetch all data from the Stocks table
        cursor.execute("SELECT * FROM Stocks")

        # Fetch all results
        rows = cursor.fetchall()

        # Print the result
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection safely
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    fetch_data()
