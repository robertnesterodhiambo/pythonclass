class User:
    @staticmethod
    def create_user(conn, firstname, lastname, email, password):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (firstname, lastname, email, password) 
            VALUES (%s, %s, %s, %s)
        """, (firstname, lastname, email, password))
        conn.commit()

    @staticmethod
    def get_user_by_email(conn, email, password):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM users WHERE email=%s AND password=%s
        """, (email, password))
        return cursor.fetchone()
