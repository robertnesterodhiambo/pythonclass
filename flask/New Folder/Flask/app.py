from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database connection details
db = mysql.connector.connect(
    host="localhost",
    user="root",
    # password="12345",
    database="users_schema"
)

# Default route to load the 'create.html' form automatically
@app.route('/')
def home():
    return redirect('/users/new')

# Route to display all users (Read)
@app.route('/users')
def read_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, CONCAT(first_name, ' ', last_name) AS full_name, email, created_at FROM users_schema")
    users = cursor.fetchall()
    return render_template('read.html', users=users)

# Route to show the create user form
@app.route('/users/new')
def new_user_form():
    return render_template('create.html')

# Route to handle form submission and insert user into database
@app.route('/users/create', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    cursor = db.cursor()
    sql = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (first_name, last_name, email, datetime.now(), datetime.now()))
    db.commit()
    return redirect('/users')  # Redirect to the users list after creating a new user

if __name__ == '__main__':
    app.run(debug=True)
