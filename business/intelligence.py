from business.models import Business

from lead_engine.database import load_businesses
from crm.database import load_crm_data


def load_business_intelligence():

    businesses = []

    lead_df = load_businesses()

    crm_df = load_crm_data()

    if lead_df.empty:

        return businesses

    for _, row in lead_df.iterrows():

        business = Business()

        business.id = row.get("id")

        business.name = row.get("name", "")

        business.website = row.get("website", "")

        business.phone = row.get("phone", "")

        business.address = row.get("address", "")

        business.city = row.get("city", "")

        business.business_type = row.get("business_type", "")

        business.lead_score = row.get("lead_score", 0)

        business.opportunity = row.get("opportunity", "")

        if not crm_df.empty:

            crm = crm_df[
                crm_df["business_id"] == business.id
            ]

            if not crm.empty:

                crm = crm.iloc[0]

                business.status = crm["status"]

                business.priority = crm["priority"]

                business.assigned_to = crm["assigned_to"]

                business.proposal_sent = bool(
                    crm["proposal_sent"]
                )

                business.followup_date = crm["followup_date"]

                business.meeting_date = crm["meeting_date"]

                business.notes = crm["notes"]

                business.estimated_value = crm["estimated_value"]

                business.revenue = crm["revenue"]

                business.deal_stage = crm["deal_stage"]

        businesses.append(business)

    return businesses