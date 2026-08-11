# subscription/database.py

import sqlite3
from datetime import datetime

DB_NAME = "growthradar.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    return sqlite3.connect(
        DB_NAME
    )


# ==========================================================
# CREATE / UPGRADE SUBSCRIPTION TABLE
# ==========================================================

def create_subscription_table():

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # Create base table
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subscriptions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE,

            plan TEXT DEFAULT 'FREE',

            status TEXT DEFAULT 'ACTIVE',

            business_finder_usage INTEGER DEFAULT 0,

            website_scanner_usage INTEGER DEFAULT 0,

            crm_leads_usage INTEGER DEFAULT 0,

            proposal_writer_usage INTEGER DEFAULT 0,

            reports_usage INTEGER DEFAULT 0,

            ai_employees_usage INTEGER DEFAULT 0,

            website_builder_usage INTEGER DEFAULT 0,

            social_intelligence_usage INTEGER DEFAULT 0,

            trend_intelligence_usage INTEGER DEFAULT 0,

            renewal_date TEXT,

            expiry_date TEXT,

            usage_reset_date TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    # ------------------------------------------------------
    # Existing columns
    # ------------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(subscriptions)"
    )

    columns = [

        row[1]

        for row in cursor.fetchall()

    ]

    # ------------------------------------------------------
    # Automatic database upgrades
    # ------------------------------------------------------

    upgrades = {

        "user_email":
            "TEXT DEFAULT ''",

        "business_finder_usage":
            "INTEGER DEFAULT 0",

        "website_scanner_usage":
            "INTEGER DEFAULT 0",

        "crm_leads_usage":
            "INTEGER DEFAULT 0",

        "proposal_writer_usage":
            "INTEGER DEFAULT 0",

        "reports_usage":
            "INTEGER DEFAULT 0",

        "ai_employees_usage":
            "INTEGER DEFAULT 0",

        "website_builder_usage":
            "INTEGER DEFAULT 0",

        "social_intelligence_usage":
            "INTEGER DEFAULT 0",

        "trend_intelligence_usage":
            "INTEGER DEFAULT 0",

        "usage_reset_date":
            "TEXT",

        "renewal_date":
            "TEXT",

        "expiry_date":
            "TEXT"

    }

    for column, definition in upgrades.items():

        if column not in columns:

            cursor.execute(
                f"""
                ALTER TABLE subscriptions
                ADD COLUMN {column} {definition}
                """
            )

    conn.commit()
    conn.close()


# ==========================================================
# CREATE DEFAULT SUBSCRIPTION
# ==========================================================

def create_default_subscription(
    email
):

    if not email:

        return False

    create_subscription_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO subscriptions(

            email,
            plan,
            status,
            usage_reset_date

        )

        VALUES(

            ?,
            'FREE',
            'ACTIVE',
            ?

        )
        """,
        (
            email,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )
    )

    conn.commit()
    conn.close()

    return True


# ==========================================================
# GET SUBSCRIPTION
# ==========================================================

def get_subscription(
    email
):

    if not email:

        return None

    create_subscription_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM subscriptions

        WHERE email=?

        """,
        (
            email,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================================================
# UPDATE PLAN
# ==========================================================

def update_plan(
    email,
    plan
):

    if not email:

        return False

    if not plan:

        return False

    create_subscription_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE subscriptions

        SET

            plan=?,

            status='ACTIVE',

            usage_reset_date=?

        WHERE email=?

        """,
        (
            plan.upper(),

            datetime.now().strftime(
                "%Y-%m-%d"
            ),

            email

        )
    )

    conn.commit()

    updated = (
        cursor.rowcount > 0
    )

    conn.close()

    return updated


# ==========================================================
# GET FEATURE USAGE
# ==========================================================

def get_feature_usage(
    email,
    feature
):

    if not email:

        return 0

    if not feature:

        return 0

    create_subscription_table()

    allowed_features = {

        "business_finder",

        "website_scanner",

        "crm_leads",

        "proposal_writer",

        "reports",

        "ai_employees",

        "website_builder",

        "social_intelligence",

        "trend_intelligence"

    }

    if feature not in allowed_features:

        return 0

    column = (
        f"{feature}_usage"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT {column}

        FROM subscriptions

        WHERE email=?

        """,
        (
            email,
        )
    )

    row = cursor.fetchone()

    conn.close()

    if not row:

        return 0

    try:

        return int(
            row[0] or 0
        )

    except Exception:

        return 0


# ==========================================================
# INCREASE FEATURE USAGE
# ==========================================================

def increase_feature_usage(
    email,
    feature
):

    if not email:

        return False

    if not feature:

        return False

    create_subscription_table()

    allowed_features = {

        "business_finder",

        "website_scanner",

        "crm_leads",

        "proposal_writer",

        "reports",

        "ai_employees",

        "website_builder",

        "social_intelligence",

        "trend_intelligence"

    }

    if feature not in allowed_features:

        return False

    column = (
        f"{feature}_usage"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE subscriptions

        SET {column} =
            COALESCE(
                {column},
                0
            ) + 1

        WHERE email=?

        """,
        (
            email,
        )
    )

    conn.commit()

    updated = (
        cursor.rowcount > 0
    )

    conn.close()

    return updated


# ==========================================================
# RESET FEATURE USAGE
# ==========================================================

def reset_feature_usage(
    email,
    feature
):

    if not email:

        return False

    if not feature:

        return False

    create_subscription_table()

    allowed_features = {

        "business_finder",

        "website_scanner",

        "crm_leads",

        "proposal_writer",

        "reports",

        "ai_employees",

        "website_builder",

        "social_intelligence",

        "trend_intelligence"

    }

    if feature not in allowed_features:

        return False

    column = (
        f"{feature}_usage"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE subscriptions

        SET {column}=0

        WHERE email=?

        """,
        (
            email,
        )
    )

    conn.commit()

    updated = (
        cursor.rowcount > 0
    )

    conn.close()

    return updated


# ==========================================================
# RESET ALL FEATURE USAGE
# ==========================================================

def reset_all_feature_usage(
    email
):

    if not email:

        return False

    create_subscription_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE subscriptions

        SET

            business_finder_usage=0,

            website_scanner_usage=0,

            crm_leads_usage=0,

            proposal_writer_usage=0,

            reports_usage=0,

            ai_employees_usage=0,

            website_builder_usage=0,

            social_intelligence_usage=0,

            trend_intelligence_usage=0,

            usage_reset_date=?

        WHERE email=?

        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d"
            ),

            email

        )
    )

    conn.commit()

    updated = (
        cursor.rowcount > 0
    )

    conn.close()

    return updated


# ==========================================================
# CLEAR SUBSCRIPTION
# ==========================================================

def delete_subscription(
    email
):

    if not email:

        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM subscriptions

        WHERE email=?

        """,
        (
            email,
        )
    )

    conn.commit()

    deleted = (
        cursor.rowcount > 0
    )

    conn.close()

    return deleted