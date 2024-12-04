# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost/users_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
