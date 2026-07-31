from subscriptions.plans import get_plan


def get_limit(plan_name, feature):

    plan = get_plan(plan_name)

    return plan["features"].get(feature, 0)


def is_unlimited(plan_name, feature):

    return get_limit(plan_name, feature) == -1


def can_use(plan_name, feature, current_usage):

    limit = get_limit(plan_name, feature)

    if limit == -1:
        return True

    return current_usage < limit


def remaining_usage(plan_name, feature, current_usage):

    limit = get_limit(plan_name, feature)

    if limit == -1:
        return "Unlimited"

    remaining = limit - current_usage

    if remaining < 0:
        remaining = 0

    return remaining


def upgrade_required(plan_name, feature, current_usage):

    return not can_use(
        plan_name,
        feature,
        current_usage
    )