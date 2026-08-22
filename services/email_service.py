import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()


# ==========================================================
# SMTP SETTINGS
# ==========================================================

SMTP_EMAIL = os.getenv(
    "SMTP_EMAIL"
)

SMTP_APP_PASSWORD = os.getenv(
    "SMTP_APP_PASSWORD"
)

SMTP_HOST = os.getenv(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)


# ==========================================================
# SEND EMAIL
# ==========================================================

def send_email(
    recipient,
    subject,
    body
):

    if not SMTP_EMAIL:

        return False, (
            "SMTP_EMAIL is not configured."
        )

    if not SMTP_APP_PASSWORD:

        return False, (
            "SMTP_APP_PASSWORD is not configured."
        )

    try:

        message = EmailMessage()

        message["From"] = SMTP_EMAIL

        message["To"] = recipient

        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=20
        ) as server:

            server.starttls()

            server.login(
                SMTP_EMAIL,
                SMTP_APP_PASSWORD
            )

            server.send_message(
                message
            )

        return True, (
            "Email sent successfully."
        )

    except Exception as error:

        return False, (
            f"Unable to send email: {error}"
        )