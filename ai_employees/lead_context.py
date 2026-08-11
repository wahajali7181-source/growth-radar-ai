import pandas as pd


# ==========================================================
# SAFE VALUE
# ==========================================================

def safe_value(value, default="Not available"):

    if value is None:
        return default

    try:

        if pd.isna(value):
            return default

    except Exception:
        pass

    value = str(value).strip()

    if not value:
        return default

    return value


# ==========================================================
# BUILD LEAD CONTEXT
# ==========================================================

def build_lead_context(business):

    if hasattr(business, "to_dict"):
        business = business.to_dict()

    context = {

        "business_name": safe_value(
            business.get(
                "business_name",
                business.get("name", "")
            )
        ),

        "industry": safe_value(
            business.get("industry", "")
        ),

        "location": safe_value(
            business.get("location", "")
        ),

        "website": safe_value(
            business.get("website", "")
        ),

        "email": safe_value(
            business.get("email", "")
        ),

        "phone": safe_value(
            business.get("phone", "")
        ),

        "lead_score": safe_value(
            business.get("lead_score", 0),
            "0"
        ),

        "priority": safe_value(
            business.get("priority", "")
        ),

        "status": safe_value(
            business.get("status", "")
        ),

        "notes": safe_value(
            business.get("notes", "")
        ),

        "estimated_value": safe_value(
            business.get("estimated_value", 0),
            "0"
        ),

        "deal_stage": safe_value(
            business.get("deal_stage", "")
        ),

    }

    # ======================================================
    # OPTIONAL INTELLIGENCE DATA
    # ======================================================

    optional_fields = [

        "website_score",
        "website_issues",
        "website_analysis",

        "social_score",
        "social_issues",
        "social_analysis",

        "google_reviews",
        "review_score",

        "facebook",
        "instagram",
        "linkedin",
        "tiktok",

    ]

    for field in optional_fields:

        if field in business:

            context[field] = safe_value(
                business.get(field)
            )

    return context


# ==========================================================
# CREATE AI RESEARCH SUMMARY
# ==========================================================

def build_research_summary(context):

    summary = []

    business_name = context.get(
        "business_name",
        "Business"
    )

    industry = context.get(
        "industry",
        "Unknown industry"
    )

    location = context.get(
        "location",
        "Unknown location"
    )

    summary.append(
        f"Business: {business_name}"
    )

    summary.append(
        f"Industry: {industry}"
    )

    summary.append(
        f"Location: {location}"
    )

    # ------------------------------------------------------
    # Website
    # ------------------------------------------------------

    website = context.get(
        "website",
        ""
    )

    if website != "Not available":

        summary.append(
            f"Website: {website}"
        )

    website_score = context.get(
        "website_score"
    )

    if website_score:

        summary.append(
            f"Website score: {website_score}"
        )

    website_issues = context.get(
        "website_issues"
    )

    if website_issues:

        summary.append(
            f"Website issues: {website_issues}"
        )

    # ------------------------------------------------------
    # Social
    # ------------------------------------------------------

    social_score = context.get(
        "social_score"
    )

    if social_score:

        summary.append(
            f"Social media score: {social_score}"
        )

    social_issues = context.get(
        "social_issues"
    )

    if social_issues:

        summary.append(
            f"Social media issues: {social_issues}"
        )

    # ------------------------------------------------------
    # Reviews
    # ------------------------------------------------------

    reviews = context.get(
        "google_reviews"
    )

    if reviews:

        summary.append(
            f"Google reviews: {reviews}"
        )

    review_score = context.get(
        "review_score"
    )

    if review_score:

        summary.append(
            f"Review score: {review_score}"
        )

    # ------------------------------------------------------
    # Lead score
    # ------------------------------------------------------

    summary.append(
        f"Lead score: {context.get('lead_score', '0')}"
    )

    summary.append(
        f"Priority: {context.get('priority', 'Not available')}"
    )

    return "\n".join(summary)


# ==========================================================
# FINAL AI CONTEXT
# ==========================================================

def create_ai_lead_context(business):

    context = build_lead_context(
        business
    )

    research_summary = build_research_summary(
        context
    )

    return {

        "lead": context,

        "research_summary": research_summary,

    }