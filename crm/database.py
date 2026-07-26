import sqlite3

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_crm_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crm(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        business_id INTEGER,

        starred INTEGER DEFAULT 0,

        notes TEXT,

        followup_date TEXT,

        proposal_sent INTEGER DEFAULT 0,

        status TEXT DEFAULT 'New',

        estimated_value INTEGER DEFAULT 0

    )
    """)

    conn.commit()
    conn.close()