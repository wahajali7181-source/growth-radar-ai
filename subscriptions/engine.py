from subscriptions.database import get_subscription

from subscriptions.limits import (

    can_use,

    remaining_usage,

    upgrade_required

)

from subscriptions.usage import get_usage


def get_user_plan(email):

    subscription = get_subscription(email)

    if not subscription:

        return "FREE"

    return subscription[2]


def has_access(

    email,

    feature

):

    usage = get_usage(

        email,

        feature

    )

    plan = get_user_plan(email)

    return can_use(

        plan,

        feature,

        usage

    )


def get_remaining(

    email,

    feature

):

    usage = get_usage(

        email,

        feature

    )

    plan = get_user_plan(email)

    return remaining_usage(

        plan,

        feature,

        usage

    )


def needs_upgrade(

    email,

    feature

):

    usage = get_usage(

        email,

        feature

    )

    plan = get_user_plan(email)

    return upgrade_required(

        plan,

        feature,

        usage

    )