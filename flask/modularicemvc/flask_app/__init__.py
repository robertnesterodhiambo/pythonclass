from flask import Flask
from flask_app.config.mysqlconnection import init_db

app = Flask(__name__)
app.secret_key = 'here'
# Initialize the database
init_db()

# Import routes
from flask_app.controllers import users



