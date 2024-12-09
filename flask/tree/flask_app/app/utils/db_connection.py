import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3308,
            user='root',
            password='',
            database='flask_db'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
