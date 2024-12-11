from flask_app import get_db_connection, bcrypt

class User:
    @staticmethod
    def create_user(first_name, last_name, email, password):
        connection = get_db_connection()
        cursor = connection.cursor()
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                       (first_name, last_name, email, hashed_password))
        connection.commit()
        connection.close()

    @staticmethod
    def get_user_by_email(email):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        connection.close()
        return user

    @staticmethod
    def verify_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
