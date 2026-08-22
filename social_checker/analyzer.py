import re


NOT_FOUND = "❌ Not Found"


# ==========================================================
# HELPERS
# ==========================================================

def is_valid_email(value):
    """Return True only when the value looks like a real email."""

    if not value:
        return False

    value = str(value).strip()

    if value == NOT_FOUND:
        return False

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    return bool(
        re.match(
            pattern,
            value
        )
    )


def is_found(value):
    """Check whether a checker field contains a usable result."""

    if not value:
        return False

    value = str(value).strip()

    if value == NOT_FOUND:
        return False

    return True


# ==========================================================
# SOCIAL SCORE
# ==========================================================

def calculate_social_score(result):
    """
    Calculate a simple social presence score out of 100.

    The score is based on:
    - Major social platforms
    - Contact availability
    - Website availability
    """

    score = 0

    # ------------------------------------------------------
    # MAJOR SOCIAL PLATFORMS
    # ------------------------------------------------------

    platforms = [
        "instagram",
        "facebook",
        "linkedin",
        "youtube",
        "tiktok",
        "twitter",
    ]

    platform_points = 10

    for platform in platforms:

        if is_found(
            result.get(platform)
        ):

            score += platform_points

    # ------------------------------------------------------
    # WHATSAPP
    # ------------------------------------------------------

    if is_found(
        result.get("whatsapp")
    ):

        score += 5

    # ------------------------------------------------------
    # WEBSITE
    # ------------------------------------------------------

    if result.get("website") == "✅ Found":

        score += 5

    # ------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------

    if is_valid_email(
        result.get("email")
    ):

        score += 5

    # ------------------------------------------------------
    # PHONE
    # ------------------------------------------------------

    if is_found(
        result.get("phone")
    ):

        score += 5

    # ------------------------------------------------------
    # GOOGLE MAPS
    # ------------------------------------------------------

    if is_found(
        result.get("google_maps")
    ):

        score += 5

    return min(
        score,
        100
    )


# ==========================================================
# OPPORTUNITY LEVEL
# ==========================================================

def get_social_status(score):

    if score >= 80:

        return "🟢 Strong Social Presence"

    if score >= 60:

        return "🟡 Good Social Presence"

    if score >= 40:

        return "🟠 Needs Improvement"

    return "🔴 Weak Social Presence"


# ==========================================================
# ANALYZE SOCIAL PRESENCE
# ==========================================================

def analyze_social_presence(result):

    score = calculate_social_score(
        result
    )

    status = get_social_status(
        score
    )

    platforms = [
        "instagram",
        "facebook",
        "linkedin",
        "youtube",
        "tiktok",
        "twitter",
    ]

    found_platforms = []

    missing_platforms = []

    for platform in platforms:

        if is_found(
            result.get(platform)
        ):

            found_platforms.append(
                platform
            )

        else:

            missing_platforms.append(
                platform
            )

    # ------------------------------------------------------
    # STRENGTHS
    # ------------------------------------------------------

    strengths = []

    if len(found_platforms) >= 4:

        strengths.append(
            "Strong multi-platform social presence."
        )

    elif len(found_platforms) >= 2:

        strengths.append(
            "Business has an established social presence."
        )

    if is_valid_email(
        result.get("email")
    ):

        strengths.append(
            "Public email contact is available."
        )

    if is_found(
        result.get("phone")
    ):

        strengths.append(
            "Phone contact is available."
        )

    if is_found(
        result.get("whatsapp")
    ):

        strengths.append(
            "WhatsApp contact is available."
        )

    # ------------------------------------------------------
    # WEAKNESSES
    # ------------------------------------------------------

    weaknesses = []

    if missing_platforms:

        weaknesses.append(
            "Missing social platforms: "
            + ", ".join(
                missing_platforms
            )
        )

    if not is_valid_email(
        result.get("email")
    ):

        weaknesses.append(
            "No valid public email was detected."
        )

    if not is_found(
        result.get("phone")
    ):

        weaknesses.append(
            "No phone number was detected."
        )

    # ------------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------------

    recommendations = []

    priority_platforms = [
        "instagram",
        "facebook",
        "linkedin",
        "youtube",
    ]

    for platform in priority_platforms:

        if platform in missing_platforms:

            recommendations.append(
                f"Consider establishing a "
                f"{platform.title()} presence."
            )

    if not is_valid_email(
        result.get("email")
    ):

        recommendations.append(
            "Add a visible business email "
            "to improve customer contact options."
        )

    if not is_found(
        result.get("phone")
    ):

        recommendations.append(
            "Add a visible business phone number."
        )

    # ------------------------------------------------------
    # RESULT
    # ------------------------------------------------------

    return {

        "score": score,

        "status": status,

        "found_platforms":
            found_platforms,

        "missing_platforms":
            missing_platforms,

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "recommendations":
            recommendations,
    }