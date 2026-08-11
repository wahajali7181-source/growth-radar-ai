# payment/gateway.py

import os


# ==========================================================
# LEMON SQUEEZY
# ==========================================================

LEMON_SQUEEZY_STORE_URL = os.getenv(
    "LEMON_SQUEEZY_STORE_URL",
    ""
)


# ==========================================================
# LEMON SQUEEZY CHECKOUT URLS
# ==========================================================
#
# IMPORTANT:
# Replace these with your actual Lemon Squeezy checkout URLs.
#
# Example:
# https://your-store.lemonsqueezy.com/checkout/buy/xxxx
#
# Keep them empty until your actual variants are ready.
# ==========================================================

LEMON_SQUEEZY_CHECKOUTS = {

    "STARTER": os.getenv(
        "LEMON_STARTER_CHECKOUT",
        ""
    ),

    "PROFESSIONAL": os.getenv(
        "LEMON_PROFESSIONAL_CHECKOUT",
        ""
    ),

    "AGENCY": os.getenv(
        "LEMON_AGENCY_CHECKOUT",
        ""

    ),

}


# ==========================================================
# PAYMENT METHODS
# ==========================================================

PAYMENT_METHODS = {

    "Lemon Squeezy": {

        "type": "online",

        "description": (
            "Secure online payment using "
            "Visa, Mastercard and other supported "
            "payment methods."
        ),

        "checkout_available": True

    },

    "Bank Transfer": {

        "type": "manual",

        "account_title": (
            os.getenv(
                "BANK_ACCOUNT_TITLE",
                "Growth Radar AI"
            )
        ),

        "bank_name": (
            os.getenv(
                "BANK_NAME",
                ""
            )
        ),

        "account_number": (
            os.getenv(
                "BANK_ACCOUNT_NUMBER",
                ""
            )
        ),

        "iban": (
            os.getenv(
                "BANK_IBAN",
                ""
            )
        ),

        "instructions": (
            "Transfer the subscription amount "
            "to the provided bank account and "
            "submit your transaction/reference ID "
            "for verification."
        ),

        "checkout_available": True

    }

}


# ==========================================================
# GET CHECKOUT URL
# ==========================================================

def get_checkout_url(plan_name):

    if not plan_name:

        return None

    plan_name = plan_name.upper().strip()

    return LEMON_SQUEEZY_CHECKOUTS.get(
        plan_name
    )


# ==========================================================
# CHECK ONLINE PAYMENT AVAILABILITY
# ==========================================================

def has_online_checkout(plan_name):

    url = get_checkout_url(
        plan_name
    )

    return bool(url)


# ==========================================================
# GET BANK TRANSFER DETAILS
# ==========================================================

def get_bank_transfer_details():

    return PAYMENT_METHODS.get(
        "Bank Transfer",
        {}
    )


# ==========================================================
# GET ALL PAYMENT METHODS
# ==========================================================

def get_payment_methods():

    return PAYMENT_METHODS