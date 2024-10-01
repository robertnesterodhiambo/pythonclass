from flask_app import app  # Import the app instance
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)  # Create Bcrypt object

# Home page with login and registration forms
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    # Validate first name and last name
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validate first name
    if len(first_name) < 2 or not first_name.isalpha():
        flash("First Name must be at least 2 characters and letters only.", "error")
        return redirect('/')

    # Validate last name
    if len(last_name) < 2 or not last_name.isalpha():
        flash("Last Name must be at least 2 characters and letters only.", "error")
        return redirect('/')

    # Validate email format
    if not User.validate_user({'email': email}):  # Assuming validate_user is implemented
        return redirect('/')

    # Validate password length
    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return redirect('/')

    # Check if passwords match
    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect('/')

    # Create the password hash
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # Decode to get string representation

    # Create a data dictionary to save the user
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": pw_hash
    }

    # Call the save @classmethod on User
    user_id = User.save(data)

    # Store user id into session
    session['user_id'] = user_id
    return redirect("/success")

# Login route
@app.route('/login', methods=['POST'])
def login():
    # Check if the email provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)  # Call the method to get user by email

    # User is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "error")
        return redirect("/")

    # Check if the passwords match
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # If we get False after checking the password
        flash("Invalid Email/Password", "error")
        return redirect('/')

    # If the passwords matched, set the user_id into session
    session['user_id'] = user_in_db.id
    return redirect("/success")

# Success page (only accessible when logged in)
@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('success.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
