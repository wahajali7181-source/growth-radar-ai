from lead_engine_v2.business_builder import BusinessLead


class LeadPipeline:

    def __init__(self):

        self.businesses = []

    # =====================================
    # Add Business
    # =====================================

    def add(

        self,

        business: BusinessLead

    ):

        self.businesses.append(

            business

        )

    # =====================================
    # Total
    # =====================================

    def total(self):

        return len(

            self.businesses

        )

    # =====================================
    # Export
    # =====================================

    def export(self):

        return [

            business.to_dict()

            for business in self.businesses

        ]

    # =====================================
    # Reset
    # =====================================

    def clear(self):

        self.businesses = []


pipeline = LeadPipeline()