import sqlite3
import os

DATABASE_DIR = "databases"
DATABASE_PATH = os.path.join(DATABASE_DIR, "auth.db")

os.makedirs(DATABASE_DIR, exist_ok=True)

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE
            CHECK (
                length(username) = 8
                AND username GLOB '[0-9]*'
                AND username NOT GLOB '*[^0-9]*'
            ),

        password_hash TEXT NOT NULL
    )
""")

conn.commit()
conn.close()

print(f"Created {DATABASE_PATH}")