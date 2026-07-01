def estimate_project_value(business):

    value = 0

    if not business.get("website"):
        value += 1500

    if not business.get("facebook"):
        value += 500

    if not business.get("instagram"):
        value += 500

    if not business.get("linkedin"):
        value += 700

    rating = business.get("rating")

    if rating is not None and rating < 4.5:
        value += 1000

    reviews = business.get("reviews")

    if reviews is not None and reviews < 100:
        value += 800

    return value


def recommend_services(business):

    services = []

    if not business.get("website"):
        services.append("Professional Website")

    if not business.get("facebook"):
        services.append("Facebook Marketing")

    if not business.get("instagram"):
        services.append("Instagram Marketing")

    if not business.get("linkedin"):
        services.append("LinkedIn Branding")

    if not business.get("email"):
        services.append("Lead Generation")

    if not business.get("phone"):
        services.append("CRM Setup")

    return services