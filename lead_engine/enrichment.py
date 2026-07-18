from lead_engine.detectors.technology_detector import detect_technology


class LeadEnrichment:

    """
    Lead Enrichment Engine

    Current Features
    ----------------
    ✔ Technology Detection

    Upcoming Features
    ----------------
    ✔ SEO Detection
    ✔ Security Detection
    ✔ Performance Detection
    ✔ Analytics Detection
    ✔ Pixel Detection
    """

    def enrich(self, business):

        website = business.get(
            "website",
            ""
        )

        result = {}

        # ==========================
        # Technology
        # ==========================

        result["technology"] = detect_technology(
            website
        )["technology"]

        return result


lead_enrichment = LeadEnrichment()