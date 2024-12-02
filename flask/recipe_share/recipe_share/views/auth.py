from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models.user import User, bcrypt, mysql

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(*user_data)
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and User.validate_password(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, email, hashed_password))
            mysql.connection.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('An error occurred: {}'.format(str(e)), 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('logout.html')  # Replace with actual dashboard
