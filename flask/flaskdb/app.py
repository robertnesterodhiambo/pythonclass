from flask import Flask, render_template, request, redirect
import sqlite3
import os
import datetime

app = Flask(__name__)

# Database file name
DATABASE = 'your_database_name.db'

# Function to create the database and users table if they do not exist
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("Database and table created successfully.")
    else:
        print("Database already exists.")

# Route to display all users
@app.route('/users')
def read_all_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
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
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, datetime.datetime.now(), datetime.datetime.now()))
            conn.commit()
        
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
