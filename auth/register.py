from datetime import datetime, timedelta

from auth.database import get_connection
from auth.utils import (
    hash_password,
    is_valid_email,
    password_strength,
)
from subscriptions.database import create_default_subscription

def register_user(

    full_name,
    email,
    password,
    confirm_password

):

    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name:

        return False, "Full Name is required."

    if not is_valid_email(email):

        return False, "Invalid email address."

    ok, message = password_strength(password)

    if not ok:

        return False, message

    if password != confirm_password:

        return False, "Passwords do not match."

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE email=?",

        (email,)

    )

    if cursor.fetchone():

        conn.close()

        return False, "Email already registered."

    hashed_password = hash_password(password)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    trial_expiry = (

        datetime.now() + timedelta(days=14)

    ).strftime("%Y-%m-%d")

    cursor.execute("""

        INSERT INTO users(

            full_name,

            email,

            password,

            plan,

            subscription_status,

            role,

            created_at,

            last_login,

            trial_expiry,

            usage_count

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

    """, (

        full_name,

        email,

        hashed_password,

        "Free",

        "Active",

        "User",

        created_at,

        "",

        trial_expiry,

        0

    ))

    conn.commit()

    conn.close()
    
    create_default_subscription(email)
    
    return True, "Registration Successful!"