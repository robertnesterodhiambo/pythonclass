from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
import bcrypt
from flask_app.config.mysqlconnector import connectToMySQL


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.get_user_by_email(email)

    if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
        flash('Invalid email or password', 'error')
        return redirect('/')

    session['user_id'] = user['id']
    session['user_name'] = user['name']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect('/')
    return render_template('dashboard.html', user_name=session['user_name'])

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')  # Render the registration form

@app.route('/register', methods=['POST'])
def register_user():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Check if user already exists
    existing_user = User.get_user_by_email(email)
    if existing_user:
        flash('Email already in use', 'error')
        return redirect('/register')

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Create a new user (add to the database)
    # You will need to create a method to insert the user into the database.
    User.create_user(name, email, hashed_password)

    flash('Account created successfully, please log in.', 'success')
    return redirect('/')  # Redirect to login page
