import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",       # XAMPP default host
        user="root",            # XAMPP default user
        password="1234",        # Your XAMPP root password
        database="flask_app_db" # The database name
    )
    return conn

def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS flask_app_db")
    cursor.close()
    conn.close()

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Run database setup
create_database()
create_user_table()
