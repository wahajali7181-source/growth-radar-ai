import sqlite3


DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# CREATE / UPGRADE PAYMENTS TABLE
# ==========================================================

def create_payments_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS payments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT DEFAULT '',

            plan TEXT DEFAULT '',

            amount REAL DEFAULT 0,

            payment_method TEXT DEFAULT '',

            transaction_id TEXT DEFAULT '',

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            reviewed_at TEXT DEFAULT '',

            reviewed_by TEXT DEFAULT ''

        )
        """
    )

    # ======================================================
    # DATABASE UPGRADE
    # ======================================================

    cursor.execute(
        "PRAGMA table_info(payments)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    upgrades = {

        "user_email":
            "TEXT DEFAULT ''",

        "plan":
            "TEXT DEFAULT ''",

        "amount":
            "REAL DEFAULT 0",

        "payment_method":
            "TEXT DEFAULT ''",

        "transaction_id":
            "TEXT DEFAULT ''",

        "status":
            "TEXT DEFAULT 'Pending'",

        "created_at":
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",

        "reviewed_at":
            "TEXT DEFAULT ''",

        "reviewed_by":
            "TEXT DEFAULT ''"

    }

    for column, definition in upgrades.items():

        if column not in columns:

            cursor.execute(
                f"""
                ALTER TABLE payments
                ADD COLUMN {column} {definition}
                """
            )

    conn.commit()
    conn.close()


# ==========================================================
# CREATE PAYMENT REQUEST
# ==========================================================

def create_payment(
    user_email,
    plan,
    amount,
    payment_method,
    transaction_id=""
):

    create_payments_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO payments(

            user_email,
            plan,
            amount,
            payment_method,
            transaction_id,
            status

        )

        VALUES(

            ?,
            ?,
            ?,
            ?,
            ?,
            'Pending'

        )
        """,
        (
            user_email,
            plan,
            amount,
            payment_method,
            transaction_id
        )
    )

    conn.commit()

    payment_id = cursor.lastrowid

    conn.close()

    return payment_id


# ==========================================================
# GET USER PAYMENTS
# ==========================================================

def get_user_payments(user_email):

    create_payments_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_email,
                plan,
                amount,
                payment_method,
                transaction_id,
                status,
                created_at,
                reviewed_at,
                reviewed_by

            FROM payments

            WHERE user_email=?

            ORDER BY id DESC
            """,
            (user_email,)
        )

        rows = cursor.fetchall()

    finally:

        conn.close()

    return rows


# ==========================================================
# GET SINGLE PAYMENT
# ==========================================================

def get_payment(payment_id):

    create_payments_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_email,
                plan,
                amount,
                payment_method,
                transaction_id,
                status,
                created_at,
                reviewed_at,
                reviewed_by

            FROM payments

            WHERE id=?

            """,
            (payment_id,)
        )

        row = cursor.fetchone()

    finally:

        conn.close()

    return row


# ==========================================================
# GET ALL PAYMENT REQUESTS
# ==========================================================

def get_all_payments_requests():

    create_payments_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_email,
                plan,
                amount,
                payment_method,
                transaction_id,
                status,
                created_at,
                reviewed_at,
                reviewed_by

            FROM payments

            ORDER BY id DESC

            """
        )

        rows = cursor.fetchall()

    finally:

        conn.close()

    return rows


# ==========================================================
# APPROVE PAYMENT
# ==========================================================

def approve_payments(
    payment_id,
    admin_email
):

    create_payments_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments

        SET

            status='Approved',

            reviewed_at=CURRENT_TIMESTAMP,

            reviewed_by=?

        WHERE id=?

        AND status='Pending'

        """,
        (
            admin_email,
            payment_id
        )
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# ==========================================================
# REJECT PAYMENT
# ==========================================================

def reject_payments(
    payment_id,
    admin_email
):

    create_payments_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments

        SET

            status='Rejected',

            reviewed_at=CURRENT_TIMESTAMP,

            reviewed_by=?

        WHERE id=?

        AND status='Pending'

        """,
        (
            admin_email,
            payment_id
        )
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# ==========================================================
# UPDATE PAYMENT STATUS
# ==========================================================

def update_payment_status(
    payment_id,
    status
):

    create_payments_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments

        SET status=?

        WHERE id=?

        """,
        (
            status,
            payment_id
        )
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# ==========================================================
# VERIFY PAYMENT
# ==========================================================

def verify_payment(
    payment_id,
    admin_email=""
):

    create_payments_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments

        SET

            status='Approved',

            reviewed_at=CURRENT_TIMESTAMP,

            reviewed_by=?

        WHERE id=?

        """,
        (
            admin_email,
            payment_id
        )
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated