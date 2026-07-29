import pandas as pd


def has_value(value):

    if pd.isna(value):
        return False

    return str(value).strip() != ""


def calculate_lead_score(business):

    score = 0

    # -------------------------
    # Website
    # -------------------------

    if has_value(business.get("website")):
        score += 20

    # -------------------------
    # Phone
    # -------------------------

    if has_value(business.get("phone")):
        score += 10

    # -------------------------
    # Email
    # -------------------------

    if has_value(business.get("email")):
        score += 10

    # -------------------------
    # Facebook
    # -------------------------

    if has_value(business.get("facebook")):
        score += 5

    # -------------------------
    # Instagram
    # -------------------------

    if has_value(business.get("instagram")):
        score += 5

    # -------------------------
    # LinkedIn
    # -------------------------

    if has_value(business.get("linkedin")):
        score += 5

    # -------------------------
    # Rating
    # -------------------------

    rating = business.get("rating", 0)

    if pd.isna(rating):
        rating = 0

    rating = float(rating)

    if rating >= 4.8:
        score += 20

    elif rating >= 4.5:
        score += 15

    elif rating >= 4:
        score += 10

    # -------------------------
    # Reviews
    # -------------------------

    reviews = business.get("reviews", 0)

    if pd.isna(reviews):
        reviews = 0

    reviews = int(reviews)

    if reviews >= 500:
        score += 25

    elif reviews >= 200:
        score += 20

    elif reviews >= 100:
        score += 15

    elif reviews >= 50:
        score += 10

    return min(score, 100)


def opportunity_level(score):

    if score >= 80:
        return "🟢 Excellent"

    elif score >= 60:
        return "🟡 Good"

    elif score >= 40:
        return "🟠 Average"

    return "🔴 High Opportunity"