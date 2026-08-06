from payments.database import get_connection


def create_payment(

    email,
    plan,
    amount,
    method,
    transaction_id,
    screenshot=""

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO payments(

            email,

            plan,

            amount,

            method,

            transaction_id,

            screenshot

        )

        VALUES(?,?,?,?,?,?)

    """, (

        email,

        plan,

        amount,

        method,

        transaction_id,

        screenshot

    ))

    conn.commit()

    conn.close()

    return True


def get_user_payments(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM payments

        WHERE email=?

        ORDER BY id DESC

    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_pending_payments():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM payments

        WHERE status='Pending'

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows