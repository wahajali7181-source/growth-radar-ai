import sqlite3

DB_NAME = "growthradar.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_users_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        plan TEXT DEFAULT 'Free',

        subscription_status TEXT DEFAULT 'Active',

        role TEXT DEFAULT 'User',

        created_at TEXT,

        last_login TEXT,

        trial_expiry TEXT,

        usage_count INTEGER DEFAULT 0

    )

    """)

    conn.commit()

    conn.close()