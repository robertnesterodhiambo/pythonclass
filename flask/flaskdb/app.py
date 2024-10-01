from flask import Flask, render_template, request, redirect
import pymysql
import os
import datetime

app = Flask(__name__)

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

# Route to display all users
@app.route('/users')
def read_all_users():
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    with connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    return render_template('read.html', users=users)

# Route to render the form for creating a new user
@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        # Insert the new user into the database
        connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
                VALUES (%s, %s, %s, NOW(), NOW())
            ''', (first_name, last_name, email))
            connection.commit()
        
        # Redirect to the read page
        return redirect('/users')
    
    # If GET request, render the form
    return render_template('create.html')

# Initialize the database
init_db()

# Start by loading all users upon running the application
@app.route('/')
def index():
    return redirect('/users')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
