from lead_engine.database import create_tables
from crm.database import create_crm_table
from ui.theme import apply_theme


def initialize():

    create_tables()
    create_crm_table()
    apply_theme()