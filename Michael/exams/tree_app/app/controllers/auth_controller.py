from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..config.database import get_db_connection
from ..models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))

        conn = get_db_connection()
        User.create_user(conn, firstname, lastname, email, password)
        conn.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = User.get_user_by_email(conn, email, password)
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = f"{user['firstname']} {user['lastname']}"
            flash('Login successful!', 'success')
            return redirect(url_for('tree.dashboard'))

        flash('Invalid credentials!', 'danger')

    return render_template('login.html')
