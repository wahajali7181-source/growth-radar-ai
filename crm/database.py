import sqlite3
import pandas as pd

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

        business_name TEXT DEFAULT '',

        industry TEXT DEFAULT '',

        status TEXT DEFAULT 'New',

        priority TEXT DEFAULT 'Medium',

        assigned_to TEXT DEFAULT '',

        starred INTEGER DEFAULT 0,

        proposal_sent INTEGER DEFAULT 0,

        followup_date TEXT DEFAULT '',

        meeting_date TEXT DEFAULT '',

        notes TEXT DEFAULT '',

        estimated_value INTEGER DEFAULT 0,

        revenue INTEGER DEFAULT 0,

        deal_stage TEXT DEFAULT 'Open',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # ==========================
    # Auto Upgrade Existing CRM
    # ==========================

    cursor.execute("PRAGMA table_info(crm)")
    columns = [row[1] for row in cursor.fetchall()]

    upgrades = {

        "business_name": "TEXT DEFAULT ''",

        "industry": "TEXT DEFAULT ''",

        "priority": "TEXT DEFAULT 'Medium'",

        "assigned_to": "TEXT DEFAULT ''",

        "meeting_date": "TEXT DEFAULT ''",

        "revenue": "INTEGER DEFAULT 0",

        "deal_stage": "TEXT DEFAULT 'Open'",

        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

    }

    for column, definition in upgrades.items():

        if column not in columns:

            cursor.execute(
                f"ALTER TABLE crm ADD COLUMN {column} {definition}"
            )

    conn.commit()
    conn.close()


# ======================================
# LOAD CRM
# ======================================

def load_crm_data():

    conn = get_connection()

    try:

        df = pd.read_sql(
            "SELECT * FROM crm",
            conn
        )

    except Exception:

        df = pd.DataFrame()

    finally:

        conn.close()

    return df


# ======================================
# GET SINGLE BUSINESS CRM
# ======================================

def get_crm_by_business(business_id):

    conn = get_connection()

    try:

        df = pd.read_sql(
            "SELECT * FROM crm WHERE business_id=?",
            conn,
            params=(business_id,)
        )

    except Exception:

        df = pd.DataFrame()

    finally:

        conn.close()

    return df


# ======================================
# TOTAL CRM RECORDS
# ======================================

def total_crm():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM crm"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ======================================
# CLEAR CRM
# ======================================

def clear_crm():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM crm"
    )

    conn.commit()

    conn.close()