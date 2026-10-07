import sqlite3
import os

DATABASE_DIR = "databases"

VOTING_DB = os.path.join(DATABASE_DIR, "voting.db")
USER_DB = os.path.join(DATABASE_DIR, "user.db")

os.makedirs(DATABASE_DIR, exist_ok=True)


def create_user_database():

    if not os.path.exists(VOTING_DB):
        print(f"ERROR: {VOTING_DB} does not exist.")
        return

    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            first_name TEXT NOT NULL,

            second_name TEXT NOT NULL,

            last_name TEXT NOT NULL,

            date_of_birth TEXT NOT NULL,

            id_number TEXT NOT NULL UNIQUE
                CHECK (
                    length(id_number) = 8
                    AND id_number GLOB '[0-9]*'
                    AND id_number NOT GLOB '*[^0-9]*'
                ),

            place_of_birth TEXT NOT NULL,

            password TEXT NOT NULL,

            province TEXT NOT NULL,

            county TEXT NOT NULL,

            constituency TEXT NOT NULL,

            ward TEXT NOT NULL,

            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print(f"Created: {USER_DB}")


if __name__ == "__main__":
    create_user_database()