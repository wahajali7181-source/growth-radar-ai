import sqlite3
from pathlib import Path


# ==========================================================
# DATABASE PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "growthradar.db"


# ==========================================================
# CONNECTION
# ==========================================================

def get_connection():

    return sqlite3.connect(
        str(DB_PATH)
    )


# ==========================================================
# USERS TABLE
# ==========================================================

def create_users_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
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
        """
    )

    conn.commit()

    conn.close()


# ==========================================================
# MAKE ADMIN
# ==========================================================

def make_admin(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET role='Admin'

        WHERE email=?
        """,
        (email,)
    )

    conn.commit()

    conn.close()