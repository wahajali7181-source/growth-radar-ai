def calculate_score(lead):

    score = 0

    # ==========================
    # Website
    # ==========================

    if lead.website:
        score += 10

    # ==========================
    # Email
    # ==========================

    if lead.email:
        score += 10

    # ==========================
    # Phone
    # ==========================

    if lead.phone:
        score += 10

    # ==========================
    # Social Media
    # ==========================

    socials = [

        lead.facebook,

        lead.instagram,

        lead.linkedin,

        lead.youtube,

        lead.twitter,

    ]

    score += min(

        15,

        len(

            [

                s for s in socials

                if s

            ]

        ) * 3,

    )

    # ==========================
    # Rating
    # ==========================

    score += min(

        20,

        int(

            lead.rating * 4

        ),

    )

    # ==========================
    # Reviews
    # ==========================

    if lead.reviews >= 500:

        score += 15

    elif lead.reviews >= 100:

        score += 10

    elif lead.reviews >= 20:

        score += 5

    # ==========================
    # Technology
    # ==========================

    if lead.technology:

        score += 10

    # ==========================
    # Website Intelligence
    # ==========================

    score += int(

        (

            lead.seo_score +

            lead.performance_score +

            lead.security_score +

            lead.website_health

        ) / 40

    )

    return min(

        score,

        100

    )


def opportunity(score):

    if score >= 85:

        return "Excellent"

    if score >= 70:

        return "High"

    if score >= 50:

        return "Medium"

    return "Low"