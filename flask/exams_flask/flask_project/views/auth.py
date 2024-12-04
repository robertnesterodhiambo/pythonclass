# views/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length

# Blueprint for auth routes
auth_blueprint = Blueprint('auth', __name__)

# Registration form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Registration route
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email is already registered
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        # Hash password and store user
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

# Login route
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your email and/or password.', 'danger')
    return render_template('login.html', form=form)

# Logout route
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
