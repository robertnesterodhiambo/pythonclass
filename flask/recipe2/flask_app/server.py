from flask import Flask, render_template, request, redirect, session, flash
from config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'
bcrypt = Bcrypt(app)

# Database connection
DATABASE = 'recipe_share'

# Route: Display Login/Register page
@app.route('/')
def index():
    return render_template('register.html')

# Route: Handle Registration
@app.route('/register', methods=['POST'])
def register():
    # Extract form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validate inputs
    if len(first_name) < 2 or len(last_name) < 2:
        session['register_error'] = "First and last names must be at least 2 characters."
        return redirect('/')
    if not '@' in email or not '.' in email:
        session['register_error'] = "Invalid email format."
        return redirect('/')
    if password != confirm_password:
        session['register_error'] = "Passwords do not match."
        return redirect('/')

    # Check if email exists in the database
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email": email}
    existing_user = mysql.query_db(query, data)

    if existing_user:
        session['register_error'] = "Email already registered. Please log in."
        return redirect('/')

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password)

    # Insert the new user into the database
    query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
    """
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password,
    }
    mysql.query_db(query, data)

    flash("Registration successful! Please log in.")
    return redirect('/login')

# Route: Display Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route: Handle Login
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    # Check if email exists in the database
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email": email}
    user = mysql.query_db(query, data)

    if not user or not bcrypt.check_password_hash(user[0]['password'], password):
        session['login_error'] = "Invalid email or password."
        return redirect('/login')

    # Store user in session
    session['user_id'] = user[0]['id']
    session['user_first_name'] = user[0]['first_name']
    return redirect('/dashboard')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Route: Dashboard (after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    # Retrieve user info and display dashboard
    mysql = connectToMySQL(DATABASE)
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {"id": session['user_id']}
    user = mysql.query_db(query, data)

    return render_template('dashboard.html', user=user[0])

if __name__ == "__main__":
    app.run(debug=True)
