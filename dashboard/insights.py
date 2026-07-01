import pandas as pd


def generate_dashboard_insights(df: pd.DataFrame):

    insights = []

    if df.empty:
        return insights

    # High opportunity leads
    high = len(df[df["lead_score"] >= 80])

    if high:
        insights.append(
            f"🔥 {high} high-value businesses found."
        )

    # No website
    no_website = len(
        df[
            df["website"].fillna("").astype(str).str.strip() == ""
        ]
    )

    if no_website:
        insights.append(
            f"🌐 {no_website} businesses have no website."
        )

    # Low reviews
    low_reviews = len(
        df[
            df["reviews"].fillna(0) < 50
        ]
    )

    if low_reviews:
        insights.append(
            f"⭐ {low_reviews} businesses need more Google reviews."
        )

    return insights