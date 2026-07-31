import sqlite3

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_payments_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        plan TEXT,

        amount REAL,

        method TEXT,

        transaction_id TEXT,

        status TEXT DEFAULT 'Pending',

        screenshot TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()