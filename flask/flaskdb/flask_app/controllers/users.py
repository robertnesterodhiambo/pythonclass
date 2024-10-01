from flask import render_template, request, redirect, flash
from flask_app import app
from flask_app.models.user import User

# Route to display all users
@app.route('/users')
def read_all_users():
    users = User.get_all_users()
    return render_template('read.html', users=users)

# Route to render the form for creating a new user
@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        # Validate user input
        if len(first_name) < 2 or not first_name.isalpha():
            flash("First Name must be at least 2 characters and letters only.", "error")
            return redirect('/users/new')

        if len(last_name) < 2 or not last_name.isalpha():
            flash("Last Name must be at least 2 characters and letters only.", "error")
            return redirect('/users/new')

        if not User.validate_user({'email': email}):
            return redirect('/users/new')

        # Insert the new user into the database
        if User.create_user(first_name, last_name, email):
            return redirect('/users')
        else:
            flash("An error occurred while creating the user.", "error")
            return redirect('/users/new')
    
    # If GET request, render the form
    return render_template('create.html')
