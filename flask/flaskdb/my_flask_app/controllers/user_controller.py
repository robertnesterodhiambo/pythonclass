# controllers/user_controller.py

from flask import Blueprint, render_template, request, redirect
from models.user_model import get_all_users, create_user, init_db

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users')
def read_all_users():
    users = get_all_users()
    return render_template('read.html', users=users)

@user_controller.route('/users/new', methods=['GET', 'POST'])
def create_user_view():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        create_user(first_name, last_name, email)
        return redirect('/users')
    
    return render_template('create.html')

@user_controller.route('/')
def index():
    return redirect('/users')
