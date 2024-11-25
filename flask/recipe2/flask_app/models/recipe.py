from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'recipe_share'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_cooked = data['date_cooked']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, under_30_minutes, date_cooked, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30_minutes)s, %(date_cooked)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT recipes.*, users.first_name AS posted_by
        FROM recipes
        JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            recipe.posted_by = row['posted_by']
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db({'id': id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes
        SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30_minutes=%(under_30_minutes)s, date_cooked=%(date_cooked)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db({'id': id})

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(form['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(form['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        if 'date_cooked' not in form or not form['date_cooked']:
            flash("Date must not be blank.")
            is_valid = False
        return is_valid
