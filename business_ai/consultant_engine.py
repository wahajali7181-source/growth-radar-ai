def analyze_business(

    business_name,
    industry,
    website,
    location

):

    health = 40

    strengths = []

    weaknesses = []

    services = []

    if website:

        health += 25

        strengths.append(
            "Website Available"
        )

    else:

        weaknesses.append(
            "No Website"
        )

        services.append(
            "Website Development"
        )

    industry = industry.lower()

    if industry == "dentist":

        services += [

            "Local SEO",
            "Google Ads",
            "Meta Ads"

        ]

    elif industry == "real estate":

        services += [

            "Lead Generation",
            "Meta Ads",
            "Landing Pages"

        ]

    elif industry == "restaurant":

        services += [

            "Social Media",
            "Food Photography",
            "Meta Ads"

        ]

    else:

        services += [

            "SEO",
            "Digital Marketing"

        ]

    weaknesses.append(
        "Growth Strategy Needed"
    )

    revenue = f"${health * 100}"

    priority = (

        "HIGH"

        if health < 70

        else "MEDIUM"

    )

    closing = min(

        health + 20,

        95

    )

    return {

        "health": health,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "services": list(set(services)),

        "revenue": revenue,

        "priority": priority,

        "closing": closing

    }