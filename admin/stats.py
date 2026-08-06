from auth.database import get_connection


def total_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def premium_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM subscriptions

        WHERE plan!='FREE'

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def free_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM subscriptions

        WHERE plan='FREE'

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total