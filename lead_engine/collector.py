import pandas as pd

from local_business_finder.finder import find_businesses
from lead_engine.contact_discovery import discover_contacts
from lead_engine.enrichment import lead_enrichment


class BusinessCollector:
    """
    Collects businesses from all available sources.

    Current Sources
    ----------------
    - Google Places
    - OpenStreetMap

    Future Sources
    ----------------
    - Yelp
    - Bing
    - Facebook
    - LinkedIn
    - Yellow Pages
    """

    def __init__(self):

        self.sources = [
            self.collect_local
        ]

    def collect_local(
        self,
        business_type,
        city
    ):

        return find_businesses(
            business_type,
            city
        )

    def enrich_contacts(
        self,
        df
    ):

        if df.empty:
            return df

        emails = []
        phones = []
        facebook = []
        instagram = []
        linkedin = []
        youtube = []
        twitter = []

        for _, business in df.iterrows():

            website = business.get(
                "website",
                ""
            )

            contacts = discover_contacts(
                website
            )

            emails.append(
                ", ".join(
                    contacts["emails"]
                )
            )

            phones.append(
                ", ".join(
                    contacts["phones"]
                )
            )

            socials = contacts["socials"]

            facebook.append(
                socials.get(
                    "facebook",
                    ""
                )
            )

            instagram.append(
                socials.get(
                    "instagram",
                    ""
                )
            )

            linkedin.append(
                socials.get(
                    "linkedin",
                    ""
                )
            )

            youtube.append(
                socials.get(
                    "youtube",
                    ""
                )
            )

            twitter.append(
                socials.get(
                    "twitter",
                    ""
                )
            )

        df["email"] = emails
        df["phone"] = phones
        df["facebook"] = facebook
        df["instagram"] = instagram
        df["linkedin"] = linkedin
        df["youtube"] = youtube
        df["twitter"] = twitter
        technologies = []

        for _, business in df.iterrows():

            enriched = lead_enrichment.enrich(
                business
    )

            technologies.append(
                enriched["technology"]
    )

        df["technology"] = technologies

        return df

    def collect(
        self,
        business_type,
        city
    ):

        all_results = []

        for source in self.sources:

            try:

                df = source(
                    business_type,
                    city
                )

                if (
                    df is not None
                    and
                    not df.empty
                ):

                    all_results.append(df)

            except Exception as e:

                print(
                    f"Collector Error: {e}"
                )

        if not all_results:

            return pd.DataFrame()

        combined = pd.concat(
            all_results,
            ignore_index=True
        )

        combined = self.enrich_contacts(
            combined
        )

        return combined


collector = BusinessCollector()


def collect_businesses(
    business_type,
    city
):

    return collector.collect(
        business_type,
        city
    )