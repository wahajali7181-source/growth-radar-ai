from datetime import datetime

from auth.database import get_connection
from auth.utils import verify_password


def login_user(email, password):

    email = email.strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            full_name,
            email,
            password,
            plan,
            role
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()

    if not user:

        conn.close()
        return False, "Invalid email or password."

    if not verify_password(password, user[3]):

        conn.close()
        return False, "Invalid email or password."

    last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE users
        SET last_login=?
        WHERE id=?
        """,
        (last_login, user[0])
    )

    conn.commit()
    conn.close()

    return True, {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "plan": user[4],
        "role": user[5]
    }