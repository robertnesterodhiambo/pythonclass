from flask import request, redirect, render_template, session, flash
from flask_app import app, db
from flask_app.models.user import User

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')

        hashed_password = User.hash_password(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created successfully!", "success")
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and User.verify_password(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect('/dashboard')
        
        flash("Invalid email or password", "error")
        return redirect('/login')

    return render_template('login.html')
