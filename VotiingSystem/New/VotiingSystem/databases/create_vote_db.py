import sqlite3
import os

DATABASE_DIR = "databases"
DATABASE_PATH = os.path.join(DATABASE_DIR, "vote.db")

os.makedirs(DATABASE_DIR, exist_ok=True)

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        id_number TEXT NOT NULL UNIQUE
            CHECK (
                length(id_number) = 8
                AND id_number GLOB '[0-9]*'
                AND id_number NOT GLOB '*[^0-9]*'
            ),

        president_vote INTEGER NOT NULL,

        governor_vote INTEGER NOT NULL,

        senator_vote INTEGER NOT NULL,

        women_rep_vote INTEGER NOT NULL,

        mp_vote INTEGER NOT NULL,

        mca_vote INTEGER NOT NULL,

        province INTEGER NOT NULL,

        county INTEGER NOT NULL,

        constituency INTEGER NOT NULL,

        ward INTEGER NOT NULL,

        created_at TEXT NOT NULL
            DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()

print(f"Created: {DATABASE_PATH}")