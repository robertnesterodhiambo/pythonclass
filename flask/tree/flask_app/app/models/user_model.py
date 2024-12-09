from app.utils.db_connection import get_db_connection
from app.utils.password_utils import hash_password, check_password

def create_user(first_name, last_name, email, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
    ''', (first_name, last_name, email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

def check_user_credentials(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
    stored_hash = cursor.fetchone()
    cursor.close()
    conn.close()

    if stored_hash:
        return check_password(stored_hash[0], password)
    return False

