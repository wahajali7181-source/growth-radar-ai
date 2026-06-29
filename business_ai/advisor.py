import pandas as pd


def get_business_advice(business):

    advice = []

    # =========================
    # Website
    # =========================
    website = str(business.get("website", "")).strip()

    if not website:
        advice.append("• Build a professional website.")

    # =========================
    # Rating
    # =========================
    rating = business.get("rating", 0)

    if pd.isna(rating):
        rating = 0

    rating = float(rating)

    if rating < 4.5:
        advice.append(
            "• Improve customer reviews and online reputation."
        )

    # =========================
    # Reviews
    # =========================
    reviews = business.get("reviews", 0)

    if pd.isna(reviews):
        reviews = 0

    reviews = int(reviews)

    if reviews < 100:
        advice.append(
            "• Increase Google reviews to improve trust."
        )

    # =========================
    # Lead Score
    # =========================
    lead_score = business.get("lead_score", 0)

    if pd.isna(lead_score):
        lead_score = 0

    lead_score = int(lead_score)

    if lead_score >= 80:
        advice.append(
            "• Excellent lead. Contact immediately."
        )

    elif lead_score >= 60:
        advice.append(
            "• Good opportunity for SEO and Meta Ads."
        )

    else:
        advice.append(
            "• Needs a complete digital marketing strategy."
        )

    return "\n".join(advice)