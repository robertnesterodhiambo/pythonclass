from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import create_user, check_user_credentials

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('user.register'))

        # Create user in database
        create_user(first_name, last_name, email, password)
        flash("Account created successfully!", 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if check_user_credentials(email, password):
            session['user'] = email  # Store user in session to indicate they are logged in
            flash("Login successful!", 'success')
            return redirect(url_for('user.dashboard'))  # Redirecting to dashboard after successful login
        else:
            flash("Invalid email or password!", 'danger')

    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session to log them out
    flash("You have been logged out.", 'success')
    return redirect(url_for('user.login'))  # Redirect to login page after logging out

@user_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('user.login'))  # Ensure user is logged in before accessing dashboard

    return render_template('dashboard.html')  # Replace with actual dashboard page


from flask_login import login_user, logout_user, current_user

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = check_user_credentials(email, password)
        if user:
            login_user(user)  # This will log the user in and manage session
            flash("Login successful!", 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash("Invalid email or password!", 'danger')

    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    logout_user()  # This will log the user out
    flash("You have been logged out.", 'success')
    return redirect(url_for('user.login'))
