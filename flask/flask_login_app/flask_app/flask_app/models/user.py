import re  # the regex module
from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash

# Create a regular expression object for validating email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        return connect_to_mysql('flask_login').query_db(query, (data['first_name'], data['last_name'], data['email'], data['password']))

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %s;"
        result = connect_to_mysql('flask_login').query_db(query, (data['email'],))

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        
        # Validate email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "error")
            is_valid = False
            
        return is_valid
