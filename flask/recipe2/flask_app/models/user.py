from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    db_name = 'recipe_share'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'email': email})
        if not result:
            return None
        return cls(result[0])

    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not form['email']:
            flash("Invalid email address.")
            is_valid = False
        if len(form['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if form['password'] != form['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
