from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    User.save(data)
    session['user_id'] = User.get_by_email(data['email']).id
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
