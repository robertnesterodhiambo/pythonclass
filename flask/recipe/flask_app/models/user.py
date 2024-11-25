from flask_app.config.mysqlconnector import connectToMySQL

class User:
    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        connection = connectToMySQL('Flask')  # Replace with your database name
        cursor = connection.cursor()
        cursor.execute(query, data)
        result = cursor.fetchone()
        connection.close()
        return result

    @staticmethod
    def create_user(name, email, password):
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s);"
        data = {
            "name": name,
            "email": email,
            "password": password
        }
        connection = connectToMySQL('Flask')  # Replace with your database name
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        connection.close()
