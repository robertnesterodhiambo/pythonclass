from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
import bcrypt  # For password hashing

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
