import pymysql
from flask_app.config.mysqlconnection import HOST, USER, PASSWORD, DATABASE
import re
from flask import flash

# Create a regular expression object for validating email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    @staticmethod
    def get_all_users():
        connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
        return users

    @staticmethod
    def create_user(first_name, last_name, email):
        connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        try:
            with connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
                    VALUES (%s, %s, %s, NOW(), NOW())
                ''', (first_name, last_name, email))
                connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def validate_user(user):
        is_valid = True
        
        # Validate email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "error")
            is_valid = False
            
        return is_valid
