def get_upgrade_url(plan):

    plans = {

        "STARTER": "#",

        "PROFESSIONAL": "#",

        "AGENCY": "#"

    }

    return plans.get(plan.upper(), "#")


def open_checkout(plan):

    return get_upgrade_url(plan)