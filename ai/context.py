from lead_engine.database import load_businesses
from crm.database import load_crm_data


def build_context():

    context = {}

    # -----------------------------
    # Businesses
    # -----------------------------

    businesses = load_businesses()

    if businesses.empty:

        context["businesses"] = []

    else:

        context["businesses"] = businesses.to_dict("records")

    # -----------------------------
    # CRM
    # -----------------------------

    crm = load_crm_data()

    if crm.empty:

        context["crm"] = []

    else:

        context["crm"] = crm.to_dict("records")

    return context