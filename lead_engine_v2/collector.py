import pandas as pd

from local_business_finder.finder import find_businesses

from lead_engine_v2.business_builder import BusinessLead
from lead_engine_v2.pipeline import pipeline
from lead_engine_v2.enrichment import enrich_business
from lead_engine_v2.website_intelligence import enrich_website
from lead_engine_v2.scoring import calculate_score, opportunity


class LeadCollector:

    def collect(

        self,

        business_type,

        city

    ):

        pipeline.clear()

        df = find_businesses(

            business_type,

            city

        )

        if df is None or df.empty:

            return pd.DataFrame()

        for _, row in df.iterrows():

            lead = BusinessLead(

                name=row.get("name", ""),

                business_type=business_type,

                city=city,

                address=row.get("address", ""),

                website=row.get("website", ""),

                phone=row.get("phone", ""),

                rating=float(row.get("rating", 0) or 0),

                reviews=int(row.get("reviews", 0) or 0),

                source="Google Places"

            )

            # -----------------------------
            # Contact Discovery
            # -----------------------------

            lead = enrich_business(lead)

            # -----------------------------
            # Website Intelligence
            # -----------------------------

            lead = enrich_website(lead)

            # -----------------------------
            # AI Lead Score
            # -----------------------------

            lead.lead_score = calculate_score(lead)

            lead.opportunity = opportunity(

                lead.lead_score

            )

            pipeline.add(

                lead

            )

        return pd.DataFrame(

            pipeline.export()

        )


collector = LeadCollector()


def collect_businesses(

    business_type,

    city

):

    return collector.collect(

        business_type,

        city

    )