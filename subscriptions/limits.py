from subscriptions.plans import get_plan


# ==========================================================
# GET FEATURE LIMIT
# ==========================================================

def get_limit(
    plan_name,
    feature
):

    plan = get_plan(plan_name)

    features = plan.get(
        "features",
        {}
    )

    return features.get(
        feature,
        0
    )


# ==========================================================
# CHECK BOOLEAN FEATURE
# ==========================================================

def feature_enabled(
    plan_name,
    feature
):

    value = get_limit(
        plan_name,
        feature
    )

    return (
        isinstance(value, bool)
        and value is True
    )


# ==========================================================
# CHECK UNLIMITED
# ==========================================================

def is_unlimited(
    plan_name,
    feature
):

    return (
        get_limit(
            plan_name,
            feature
        ) == -1
    )


# ==========================================================
# CAN USE FEATURE
# ==========================================================

def can_use(
    plan_name,
    feature,
    current_usage=0
):

    limit = get_limit(
        plan_name,
        feature
    )

    # ------------------------------------------------------
    # BOOLEAN FEATURE
    # ------------------------------------------------------

    if isinstance(
        limit,
        bool
    ):

        return limit

    # ------------------------------------------------------
    # UNLIMITED
    # ------------------------------------------------------

    if limit == -1:

        return True

    # ------------------------------------------------------
    # INVALID / DISABLED
    # ------------------------------------------------------

    if not isinstance(
        limit,
        (int, float)
    ):

        return False

    if limit <= 0:

        return False

    # ------------------------------------------------------
    # NORMAL USAGE
    # ------------------------------------------------------

    try:

        current_usage = int(
            current_usage
        )

    except (
        TypeError,
        ValueError
    ):

        current_usage = 0

    return current_usage < limit


# ==========================================================
# REMAINING USAGE
# ==========================================================

def remaining_usage(
    plan_name,
    feature,
    current_usage=0
):

    limit = get_limit(
        plan_name,
        feature
    )

    # ------------------------------------------------------
    # BOOLEAN
    # ------------------------------------------------------

    if isinstance(
        limit,
        bool
    ):

        if limit:

            return "Available"

        return 0

    # ------------------------------------------------------
    # UNLIMITED
    # ------------------------------------------------------

    if limit == -1:

        return "Unlimited"

    # ------------------------------------------------------
    # INVALID
    # ------------------------------------------------------

    if not isinstance(
        limit,
        (int, float)
    ):

        return 0

    if limit <= 0:

        return 0

    # ------------------------------------------------------
    # CALCULATE
    # ------------------------------------------------------

    try:

        current_usage = int(
            current_usage
        )

    except (
        TypeError,
        ValueError
    ):

        current_usage = 0

    remaining = (
        limit
        - current_usage
    )

    return max(
        0,
        remaining
    )


# ==========================================================
# USAGE PERCENTAGE
# ==========================================================

def usage_percentage(
    plan_name,
    feature,
    current_usage=0
):

    limit = get_limit(
        plan_name,
        feature
    )

    # Unlimited

    if limit == -1:

        return 0

    # Boolean

    if isinstance(
        limit,
        bool
    ):

        return 0

    # Disabled / invalid

    if not isinstance(
        limit,
        (int, float)
    ):

        return 100

    if limit <= 0:

        return 100

    try:

        current_usage = int(
            current_usage
        )

    except (
        TypeError,
        ValueError
    ):

        current_usage = 0

    percentage = (
        current_usage
        / limit
    ) * 100

    return min(
        100,
        max(
            0,
            percentage
        )
    )


# ==========================================================
# UPGRADE REQUIRED
# ==========================================================

def upgrade_required(
    plan_name,
    feature,
    current_usage=0
):

    return not can_use(
        plan_name,
        feature,
        current_usage
    )


# ==========================================================
# COMPLETE LIMIT STATUS
# ==========================================================

def get_limit_status(
    plan_name,
    feature,
    current_usage=0
):

    limit = get_limit(
        plan_name,
        feature
    )

    unlimited = (
        limit == -1
    )

    boolean_feature = isinstance(
        limit,
        bool
    )

    allowed = can_use(
        plan_name,
        feature,
        current_usage
    )

    remaining = remaining_usage(
        plan_name,
        feature,
        current_usage
    )

    return {

        "plan": str(
            plan_name or "FREE"
        ).upper(),

        "feature": feature,

        "limit": limit,

        "usage": current_usage,

        "remaining": remaining,

        "allowed": allowed,

        "unlimited": unlimited,

        "boolean": boolean_feature,

        "enabled": (
            limit is True
            if boolean_feature
            else None
        ),

        "percentage": usage_percentage(
            plan_name,
            feature,
            current_usage
        )

    }