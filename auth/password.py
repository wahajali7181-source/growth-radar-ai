import hashlib
import os
import secrets
from datetime import datetime, timedelta

from auth.database import get_connection
from auth.utils import (
    hash_password,
    password_strength,
)
from services.email_service import send_email


# ==========================================================
# RESET TOKEN SETTINGS
# ==========================================================

RESET_TOKEN_EXPIRY_MINUTES = 30


# ==========================================================
# CREATE RESET TOKEN
# ==========================================================

def create_reset_token(email):

    email = email.strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()

    if not user:

        conn.close()

        return False, None

    user_id = user[0]

    # ------------------------------------------------------
    # INVALIDATE PREVIOUS UNUSED TOKENS
    # ------------------------------------------------------

    cursor.execute(
        """
        UPDATE password_reset_tokens

        SET used=1

        WHERE user_id=?

        AND used=0
        """,
        (user_id,)
    )

    # ------------------------------------------------------
    # GENERATE SECURE TOKEN
    # ------------------------------------------------------

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    created_at = datetime.now()

    expires_at = (
        created_at
        + timedelta(
            minutes=RESET_TOKEN_EXPIRY_MINUTES
        )
    )

    cursor.execute(
        """
        INSERT INTO password_reset_tokens(

            user_id,
            token_hash,
            expires_at,
            used,
            created_at

        )

        VALUES(?,?,?,?,?)
        """,
        (
            user_id,
            token_hash,
            expires_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            0,
            created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()

    # ------------------------------------------------------
    # CREATE RESET URL
    # ------------------------------------------------------

    app_base_url = os.getenv(
        "APP_BASE_URL",
        "http://localhost:8501"
    ).rstrip("/")

    reset_url = (
        f"{app_base_url}"
        f"/?token={token}"
    )

    # ------------------------------------------------------
    # SEND EMAIL
    # ------------------------------------------------------

    email_sent = send_reset_email(
        email,
        reset_url
    )

    if not email_sent:

        return False, None

    return True, None


# ==========================================================
# VERIFY RESET TOKEN
# ==========================================================

def verify_reset_token(token):

    if not token:

        return False, None

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_id,
            expires_at,
            used
        FROM password_reset_tokens
        WHERE token_hash=?
        """,
        (token_hash,)
    )

    reset_token = cursor.fetchone()

    if not reset_token:

        conn.close()

        return False, None

    token_id = reset_token[0]
    user_id = reset_token[1]
    expires_at = reset_token[2]
    used = reset_token[3]

    # ------------------------------------------------------
    # ALREADY USED
    # ------------------------------------------------------

    if used:

        conn.close()

        return False, None

    # ------------------------------------------------------
    # CHECK EXPIRY
    # ------------------------------------------------------

    try:

        expiry_datetime = datetime.strptime(
            expires_at,
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:

        conn.close()

        return False, None

    if datetime.now() > expiry_datetime:

        # Mark expired token as used
        cursor.execute(
            """
            UPDATE password_reset_tokens

            SET used=1

            WHERE id=?
            """,
            (token_id,)
        )

        conn.commit()
        conn.close()

        return False, None

    conn.close()

    return True, {
        "token_id": token_id,
        "user_id": user_id
    }


# ==========================================================
# RESET PASSWORD
# ==========================================================

def reset_password(
    token,
    new_password,
    confirm_password
):

    if not token:

        return False, "Invalid reset link."

    if new_password != confirm_password:

        return False, "Passwords do not match."

    # ------------------------------------------------------
    # PASSWORD VALIDATION
    # ------------------------------------------------------

    ok, message = password_strength(
        new_password
    )

    if not ok:

        return False, message

    # ------------------------------------------------------
    # VERIFY TOKEN
    # ------------------------------------------------------

    valid, token_data = verify_reset_token(
        token
    )

    if not valid:

        return False, (
            "This password reset link is "
            "invalid or expired."
        )

    token_id = token_data["token_id"]
    user_id = token_data["user_id"]

    hashed_password = hash_password(
        new_password
    )

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # UPDATE PASSWORD
    # ------------------------------------------------------

    cursor.execute(
        """
        UPDATE users

        SET password=?

        WHERE id=?
        """,
        (
            hashed_password,
            user_id
        )
    )

    # ------------------------------------------------------
    # MARK TOKEN AS USED
    # ------------------------------------------------------

    cursor.execute(
        """
        UPDATE password_reset_tokens

        SET used=1

        WHERE id=?
        """,
        (token_id,)
    )

    conn.commit()
    conn.close()

    return True, (
        "Password reset successfully."
    )


# ==========================================================
# SEND RESET EMAIL
# ==========================================================

def send_reset_email(
    email,
    reset_url
):

    subject = (
        "Reset your Growth Radar AI password"
    )

    body = f"""
Hello,

We received a request to reset your
Growth Radar AI password.

Use the link below to create a new password:

{reset_url}

This link will expire in
{RESET_TOKEN_EXPIRY_MINUTES} minutes.

If you did not request a password reset,
you can safely ignore this email.

Regards,

Growth Radar AI
"""

    return send_email(
        email,
        subject,
        body
    )