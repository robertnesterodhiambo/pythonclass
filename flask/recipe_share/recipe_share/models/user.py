from flask_login import UserMixin
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

bcrypt = Bcrypt()
mysql = MySQL()

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @staticmethod
    def find_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user_data = cursor.fetchone()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def validate_password(stored_password, provided_password):
        return bcrypt.check_password_hash(stored_password, provided_password)
