def analyze_business(

    business_name,
    industry,
    website,
    location

):

    industry = (industry or "").lower()

    health = 50

    strengths = []
    weaknesses = []
    opportunities = []
    services = []

    # ==========================================
    # Website
    # ==========================================

    if website:

        health += 20

        strengths.append(
            "Business already has a website."
        )

    else:

        health -= 10

        weaknesses.append(
            "Business has no professional website."
        )

        services.append(
            "Website Development"
        )

    # ==========================================
    # Industry Recommendations
    # ==========================================

    if industry == "dentist":

        services.extend([

            "Local SEO",

            "Google Ads",

            "Meta Ads",

            "Google Business Profile Optimization",

            "Reputation Management",

        ])

        opportunities.extend([

            "Rank for local dental searches.",

            "Increase appointment bookings.",

            "Improve Google Reviews.",

        ])

    elif industry == "real estate":

        services.extend([

            "Lead Generation",

            "Landing Pages",

            "Meta Ads",

            "CRM Automation",

            "Property Video Marketing",

        ])

        opportunities.extend([

            "Generate seller leads.",

            "Generate buyer leads.",

            "Automate follow-up.",

        ])

    elif industry == "restaurant":

        services.extend([

            "Social Media Marketing",

            "Meta Ads",

            "Google Business Optimization",

            "Food Photography",

            "Reels Marketing",

        ])

        opportunities.extend([

            "Increase dine-in traffic.",

            "Boost food delivery orders.",

            "Improve customer engagement.",

        ])

    elif industry == "gym":

        services.extend([

            "Meta Ads",

            "Transformation Video Editing",

            "Landing Pages",

            "Lead Funnel",

        ])

    else:

        services.extend([

            "SEO",

            "Google Ads",

            "Meta Ads",

            "Website Optimization",

        ])

    # ==========================================
    # Generic AI Analysis
    # ==========================================

    weaknesses.append(

        "No clear digital growth strategy."

    )

    weaknesses.append(

        "Lead generation can be improved."

    )

    strengths.append(

        "Business has growth potential."

    )

    opportunities.append(

        "AI automation can reduce manual work."

    )

    opportunities.append(

        "Digital marketing can increase revenue."

    )

    opportunities.append(

        "Better branding can improve trust."

    )

    # ==========================================
    # Scores
    # ==========================================

    health = max(

        min(

            health,

            95

        ),

        30

    )

    if health >= 85:

        priority = "LOW"

    elif health >= 70:

        priority = "MEDIUM"

    else:

        priority = "HIGH"

    closing = min(

        95,

        health + 15

    )

    revenue = f"${health * 150}"

    # ==========================================
    # Return
    # ==========================================

    return {

        "health": health,

        "priority": priority,

        "closing": closing,

        "revenue": revenue,

        "strengths": sorted(

            list(

                set(strengths)

            )

        ),

        "weaknesses": sorted(

            list(

                set(weaknesses)

            )

        ),

        "opportunities": sorted(

            list(

                set(opportunities)

            )

        ),

        "services": sorted(

            list(

                set(services)

            )

        ),

    }