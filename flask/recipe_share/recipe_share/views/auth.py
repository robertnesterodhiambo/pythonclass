from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models.user import User, bcrypt, mysql

# Initialize Flask-Login's LoginManager
auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by their ID (required by Flask-Login).
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, first_name, last_name, email, password FROM users WHERE id=%s", (user_id,)
    )
    user_data = cursor.fetchone()
    if user_data:
        return User(*user_data)
    return None

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Route for user signup.
    """
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
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)

        if not user:
            flash('No user found with this email.', 'danger')
            return redirect(url_for('auth.login'))

        if User.validate_password(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """
    Route for user logout.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    """
    Route for the user dashboard (protected).
    """
    return render_template('logout.html')  # Replace this with an actual dashboard template
