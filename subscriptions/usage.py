from subscriptions.database import (
    get_feature_usage,
    increase_feature_usage,
    reset_feature_usage,
)


# ==========================================================
# SUPPORTED USAGE FEATURES
# ==========================================================

USAGE_FEATURES = {

    "business_finder",
    "website_scanner",
    "crm_leads",
    "proposal_writer",
    "reports",
    "ai_employees",
    "website_builder",
    "social_intelligence",
    "trend_intelligence",

}


# ==========================================================
# GET USAGE
# ==========================================================

def get_usage(
    email,
    feature
):

    if not email or feature not in USAGE_FEATURES:

        return 0

    try:

        return int(
            get_feature_usage(
                email,
                feature
            )
            or 0
        )

    except Exception:

        return 0


# ==========================================================
# INCREASE USAGE
# ==========================================================

def increase_usage(
    email,
    feature
):

    if not email or feature not in USAGE_FEATURES:

        return False

    try:

        return bool(
            increase_feature_usage(
                email,
                feature
            )
        )

    except Exception:

        return False


# ==========================================================
# RESET USAGE
# ==========================================================

def reset_usage(
    email,
    feature
):

    if not email or feature not in USAGE_FEATURES:

        return False

    try:

        return bool(
            reset_feature_usage(
                email,
                feature
            )
        )

    except Exception:

        return False


# ==========================================================
# GET ALL USAGE
# ==========================================================

def get_all_usage(
    email
):

    if not email:

        return {}

    return {

        feature: get_usage(
            email,
            feature
        )

        for feature in USAGE_FEATURES

    }


# ==========================================================
# RESET ALL USAGE
# ==========================================================

def reset_all_usage(
    email
):

    if not email:

        return False

    success = True

    for feature in USAGE_FEATURES:

        if not reset_usage(
            email,
            feature
        ):

            success = False

    return success