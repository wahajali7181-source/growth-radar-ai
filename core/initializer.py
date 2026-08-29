from lead_engine.database import create_tables
from crm.database import create_crm_table
from ui.theme import apply_theme

from auth.database import (
    create_users_table,
    create_password_reset_table,
)

from subscriptions.database import create_subscription_table
from payments.database import create_payments_table
from ai.database import create_ai_tables
from website_builder.database import create_websites_table
# ==========================================================
# INITIALIZE APPLICATION
# ==========================================================

def initialize():

    # ------------------------------------------------------
    # LEAD ENGINE
    # ------------------------------------------------------

    create_tables()

    # ------------------------------------------------------
    # CRM
    # ------------------------------------------------------

    create_crm_table()

    # ------------------------------------------------------
    # AUTH / USERS
    # ------------------------------------------------------

    create_users_table()

    # ------------------------------------------------------
    # PASSWORD RESET
    # ------------------------------------------------------

    create_password_reset_table()

    # ------------------------------------------------------
    # SUBSCRIPTIONS
    # ------------------------------------------------------

    create_subscription_table()

    # ------------------------------------------------------
    # PAYMENTS
    # ------------------------------------------------------

    create_payments_table()

    # ------------------------------------------------------
    # AI
    # ------------------------------------------------------

    create_ai_tables()
        # ------------------------------------------------------
    # WEBSITE REGISTRY
    # ------------------------------------------------------
    
    create_websites_table()
    # ------------------------------------------------------
    # UI THEME
    # ------------------------------------------------------

    apply_theme()