from models.business_lead import BusinessLead


class LeadValidator:

    def __init__(self):
        pass

    def is_valid(self, lead: BusinessLead):

        # Name Required
        if not lead.name:
            return False

        # Address Required
        if not lead.address:
            return False

        # Coordinates Required
        if lead.latitude in [None, "", 0]:
            return False

        if lead.longitude in [None, "", 0]:
            return False

        return True

    def validate(self, leads):

        valid_leads = []

        for lead in leads:

            if self.is_valid(lead):

                valid_leads.append(lead)

        return valid_leads


validator = LeadValidator()