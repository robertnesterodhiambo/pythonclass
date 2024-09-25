from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
import pymysql

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management
bcrypt = Bcrypt(app)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',       # Your MySQL username
        #password='password',  # Your MySQL password
        db='flask_login',
        cursorclass=pymysql.cursors.DictCursor
    )

# Home page with login and registration forms
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    # Collect form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validation
    if len(first_name) < 2 or not first_name.isalpha():
        flash("First Name must be at least 2 characters and letters only.")
    if len(last_name) < 2 or not last_name.isalpha():
        flash("Last Name must be at least 2 characters and letters only.")
    if not email:
        flash("Email is required.")
    if len(password) < 8:
        flash("Password must be at least 8 characters.")
    if password != confirm_password:
        flash("Passwords do not match.")

    # If there are flash messages (errors), redirect back to index
    if '_flashes' in session:
        return redirect('/')

    # Hash password and insert new user
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, pw_hash))
            connection.commit()
            session['user_id'] = cursor.lastrowid
            return redirect('/success')
        except pymysql.MySQLError:
            flash("Email already exists.")
            return redirect('/')

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not bcrypt.check_password_hash(user['password'], password):
            flash("Invalid login credentials.")
            return redirect('/')

        # Login successful, store user in session
        session['user_id'] = user['id']
        return redirect('/success')

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

if __name__ == '__main__':
    app.run(debug=True)
