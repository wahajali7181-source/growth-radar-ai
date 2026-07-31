from auth.database import get_connection


# =====================================
# GET ALL USERS
# =====================================

def get_all_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            full_name,

            email,

            role,

            plan,

            subscription_status,

            created_at

        FROM users

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================
# MAKE ADMIN
# =====================================

def make_admin(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET role='Admin'

        WHERE email=?

    """, (email,))

    conn.commit()

    conn.close()


# =====================================
# SUSPEND USER
# =====================================

def suspend_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET subscription_status='Suspended'

        WHERE email=?

    """, (email,))

    conn.commit()

    conn.close()


# =====================================
# ACTIVATE USER
# =====================================

def activate_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET subscription_status='Active'

        WHERE email=?

    """, (email,))

    conn.commit()

    conn.close()


# =====================================
# DELETE USER
# =====================================

def delete_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM users WHERE email=?",

        (email,)

    )

    conn.commit()

    conn.close()