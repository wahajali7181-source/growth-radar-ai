import sqlite3
import pandas as pd


DB_NAME = "growthradar.db"


# ==========================================
# CONNECTION
# ==========================================

def get_connection():

    return sqlite3.connect(DB_NAME)


# ==========================================
# CREATE / UPGRADE CRM TABLE
# ==========================================

def create_crm_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crm(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            business_id INTEGER,

            user_email TEXT DEFAULT '',

            business_name TEXT DEFAULT '',

            industry TEXT DEFAULT '',

            website TEXT DEFAULT '',

            location TEXT DEFAULT '',

            email TEXT DEFAULT '',

            phone TEXT DEFAULT '',

            lead_score INTEGER DEFAULT 0,

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

    # ==========================================
    # CHECK EXISTING COLUMNS
    # ==========================================

    cursor.execute(
        "PRAGMA table_info(crm)"
    )

    columns = [

        row[1]
        for row in cursor.fetchall()

    ]

    # ==========================================
    # DATABASE UPGRADES
    # ==========================================

    upgrades = {

        "user_email":
            "TEXT DEFAULT ''",

        "business_name":
            "TEXT DEFAULT ''",

        "industry":
            "TEXT DEFAULT ''",

        "website":
            "TEXT DEFAULT ''",

        "location":
            "TEXT DEFAULT ''",

        "email":
            "TEXT DEFAULT ''",

        "phone":
            "TEXT DEFAULT ''",

        "lead_score":
            "INTEGER DEFAULT 0",

        "status":
            "TEXT DEFAULT 'New'",

        "priority":
            "TEXT DEFAULT 'Medium'",

        "assigned_to":
            "TEXT DEFAULT ''",

        "starred":
            "INTEGER DEFAULT 0",

        "proposal_sent":
            "INTEGER DEFAULT 0",

        "followup_date":
            "TEXT DEFAULT ''",

        "meeting_date":
            "TEXT DEFAULT ''",

        "notes":
            "TEXT DEFAULT ''",

        "estimated_value":
            "INTEGER DEFAULT 0",

        "revenue":
            "INTEGER DEFAULT 0",

        "deal_stage":
            "TEXT DEFAULT 'Open'",

        "created_at":
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

    }

    for column, definition in upgrades.items():

        if column not in columns:

            cursor.execute(

                f"""
                ALTER TABLE crm
                ADD COLUMN {column} {definition}
                """

            )

    conn.commit()
    conn.close()


# ==========================================
# LOAD CRM DATA
# ==========================================

def load_crm_data(user_email=None):

    if not user_email:

        return pd.DataFrame()

    conn = get_connection()

    try:

        df = pd.read_sql(

            """
            SELECT *
            FROM crm
            WHERE user_email=?
            ORDER BY id DESC
            """,

            conn,

            params=(user_email,)

        )

    except Exception:

        df = pd.DataFrame()

    finally:

        conn.close()

    return df


# ==========================================
# GET CRM BY BUSINESS
# ==========================================

def get_crm_by_business(

    business_id,
    user_email

):

    if not user_email:

        return pd.DataFrame()

    conn = get_connection()

    try:

        df = pd.read_sql(

            """
            SELECT *
            FROM crm
            WHERE business_id=?
            AND user_email=?
            """,

            conn,

            params=(

                business_id,
                user_email

            )

        )

    except Exception:

        df = pd.DataFrame()

    finally:

        conn.close()

    return df


# ==========================================
# TOTAL CRM RECORDS
# ==========================================

def total_crm(user_email=None):

    if not user_email:

        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT COUNT(*)
        FROM crm
        WHERE user_email=?
        """,

        (user_email,)

    )

    result = cursor.fetchone()

    total = result[0] if result else 0

    conn.close()

    return total


# ==========================================
# CLEAR USER CRM
# ==========================================

def clear_crm(user_email=None):

    if not user_email:

        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        DELETE FROM crm
        WHERE user_email=?
        """,

        (user_email,)

    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0