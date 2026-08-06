import sqlite3

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_subscription_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE,

        plan TEXT DEFAULT 'FREE',

        status TEXT DEFAULT 'ACTIVE',

        business_finder_usage INTEGER DEFAULT 0,

        website_scanner_usage INTEGER DEFAULT 0,

        proposal_usage INTEGER DEFAULT 0,

        reports_usage INTEGER DEFAULT 0,

        renewal_date TEXT,

        expiry_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


def create_default_subscription(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR IGNORE INTO subscriptions(

        email

    )

    VALUES(?)

    """, (email,))

    conn.commit()

    conn.close()


def get_subscription(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM subscriptions

    WHERE email=?

    """, (email,))

    row = cursor.fetchone()

    conn.close()

    return row


def update_plan(email, plan):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE subscriptions

    SET plan=?

    WHERE email=?

    """, (plan, email))

    conn.commit()

    conn.close()


# =====================================
# FEATURE USAGE
# =====================================

def get_feature_usage(email, feature):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        f"SELECT {feature}_usage FROM subscriptions WHERE email=?",

        (email,)

    )

    row = cursor.fetchone()

    conn.close()

    if not row:

        return 0

    return row[0]


def increase_feature_usage(email, feature):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        f"""

        UPDATE subscriptions

        SET {feature}_usage={feature}_usage+1

        WHERE email=?

        """,

        (email,)

    )

    conn.commit()

    conn.close()


def reset_feature_usage(email, feature):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        f"""

        UPDATE subscriptions

        SET {feature}_usage=0

        WHERE email=?

        """,

        (email,)

    )

    conn.commit()

    conn.close()