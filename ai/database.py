import sqlite3

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_ai_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS ai_conversations(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT NOT NULL,

        employee TEXT NOT NULL,

        title TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS ai_messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id INTEGER,

        role TEXT,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id)

        REFERENCES ai_conversations(id)

    )

    """)

    conn.commit()
    conn.close()