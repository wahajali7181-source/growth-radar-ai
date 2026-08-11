# subscriptions/engine.py

from subscriptions.database import (
    get_subscription,
    create_default_subscription,
)

from subscriptions.limits import (
    can_use,
    remaining_usage,
    upgrade_required,
    get_limit,
    get_limit_status,
)

from subscriptions.usage import (
    get_usage,
    increase_usage,
)


# ==========================================================
# GET USER PLAN
# ==========================================================

def get_user_plan(
    email
):

    if not email:

        return "FREE"

    subscription = get_subscription(
        email
    )

    if not subscription:

        create_default_subscription(
            email
        )

        subscription = get_subscription(
            email
        )

    if not subscription:

        return "FREE"

    try:

        plan = subscription[2]

    except Exception:

        return "FREE"

    if not plan:

        return "FREE"

    return str(
        plan
    ).upper()


# ==========================================================
# GET USER FEATURE USAGE
# ==========================================================

def get_feature_usage(
    email,
    feature
):

    if not email:

        return 0

    return get_usage(
        email,
        feature
    )


# ==========================================================
# CHECK FEATURE ACCESS
# ==========================================================

def check_feature_access(
    email,
    feature
):

    if not email:

        return {

            "allowed": False,

            "reason": "Authentication required.",

            "plan": "FREE",

            "feature": feature,

            "usage": 0,

            "limit": 0,

            "remaining": 0

        }

    plan = get_user_plan(
        email
    )

    usage = get_usage(
        email,
        feature
    )

    status = get_limit_status(
        plan,
        feature,
        usage
    )

    return {

        "allowed": status["allowed"],

        "reason": (

            "Access granted."

            if status["allowed"]

            else "Monthly usage limit reached."

        ),

        "plan": plan,

        "feature": feature,

        "usage": usage,

        "limit": status["limit"],

        "remaining": status["remaining"],

        "unlimited": status["unlimited"],

        "percentage": status["percentage"]

    }


# ==========================================================
# HAS ACCESS
# ==========================================================

def has_access(
    email,
    feature
):

    result = check_feature_access(
        email,
        feature
    )

    return result["allowed"]


# ==========================================================
# GET REMAINING USAGE
# ==========================================================

def get_remaining(
    email,
    feature
):

    if not email:

        return 0

    plan = get_user_plan(
        email
    )

    usage = get_usage(
        email,
        feature
    )

    return remaining_usage(
        plan,
        feature,
        usage
    )


# ==========================================================
# NEEDS UPGRADE
# ==========================================================

def needs_upgrade(
    email,
    feature
):

    if not email:

        return True

    plan = get_user_plan(
        email
    )

    usage = get_usage(
        email,
        feature
    )

    return upgrade_required(
        plan,
        feature,
        usage
    )


# ==========================================================
# GET USAGE STATUS
# ==========================================================

def usage_status(
    email,
    feature
):

    if not email:

        return {

            "plan": "FREE",

            "feature": feature,

            "usage": 0,

            "limit": 0,

            "remaining": 0,

            "allowed": False,

            "unlimited": False,

            "percentage": 100

        }

    plan = get_user_plan(
        email
    )

    usage = get_usage(
        email,
        feature
    )

    return get_limit_status(
        plan,
        feature,
        usage
    )


# ==========================================================
# CONSUME FEATURE
# ==========================================================
#
# This is the important function.
#
# It checks the limit FIRST.
# If allowed:
#
#       generate feature
#              ↓
#       increase usage
#
# Returns True when usage can proceed.
#
# ==========================================================

def consume_feature(
    email,
    feature
):

    if not email:

        return False

    access = check_feature_access(
        email,
        feature
    )

    if not access["allowed"]:

        return False

    # Boolean features such as
    # AI Employees / Website Builder
    # are also treated safely.

    result = increase_usage(
        email,
        feature
    )

    return result


# ==========================================================
# GET PLAN LIMIT
# ==========================================================

def get_feature_limit(
    email,
    feature
):

    if not email:

        return 0

    plan = get_user_plan(
        email
    )

    return get_limit(
        plan,
        feature
    )