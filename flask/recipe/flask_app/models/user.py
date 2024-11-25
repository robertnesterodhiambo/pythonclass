from flask_app.config.mysqlconnector import connectToMySQL

class User:
    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        connection = connectToMySQL('your_database_name')  # Replace with your database name
        cursor = connection.cursor()
        cursor.execute(query, data)
        result = cursor.fetchone()
        connection.close()
        return result
