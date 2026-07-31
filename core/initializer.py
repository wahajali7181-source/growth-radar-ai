from lead_engine.database import create_tables
from crm.database import create_crm_table
from ui.theme import apply_theme

from auth.database import create_users_table

from subscriptions.database import create_subscription_table
from payments.database import create_payments_table


def initialize():

    create_tables()

    create_crm_table()

    create_users_table()

    create_subscription_table()
    
    create_payments_table()

    apply_theme()