import pymysql

# Database configuration
DATABASE = 'user'
USER = 'root'
PASSWORD = ''  # Replace with your MySQL root password
HOST = 'localhost'

# Function to create the database and users table if they do not exist
def init_db():
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD)
    with connection:
        cursor = connection.cursor()
        # Create database if it does not exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        cursor.execute(f"USE {DATABASE}")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("Database and table created successfully.")
