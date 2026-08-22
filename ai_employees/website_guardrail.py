import re


# ==========================================================
# WEBSITE CLAIM GUARDRAIL
# ==========================================================

# Claims that commonly become dangerous when AI invents them.
UNSUPPORTED_CLAIM_PATTERNS = [

    r"\b\d+\+?\s*(years?|yrs?)\b",
    r"\b\d+\+?\s*(patients?|customers?|clients?|users?)\b",
    r"\b\d+\+?\s*(reviews?|appointments?|projects?)\b",

    r"\b\d+(?:\.\d+)?\s*%",
    r"\b\d+x\b",

    r"#\s*1\b",
    r"\bnumber one\b",
    r"\bbest\b",
    r"\btop[- ]?rated\b",

    r"\baward[- ]?winning\b",
    r"\baward winning\b",

    r"\bcertified\b",
    r"\blicensed\b",
    r"\baccredited\b",

    r"\bguarantee[sd]?\b",
    r"\bguaranteed\b",

    r"\bexperienced\b",
    r"\bexpert(s)?\b",

    r"\blatest technology\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bcutting[- ]edge\b",

    r"\bhundreds of\b",
    r"\bthousands of\b",

    r"\bhappy customers\b",
    r"\bhappy patients\b",

    r"\bserving .* for over\b",
    r"\btrusted by\b",
    r"\btrusted by thousands\b",
]


# ==========================================================
# PLACEHOLDER / FAKE TESTIMONIAL DETECTION
# ==========================================================

TESTIMONIAL_PATTERNS = [

    r"\btestimonial\b",
    r"\breview\b",
    r"\b5[- ]star\b",
    r"\bfive[- ]star\b",
    r"\bhappy patient\b",
    r"\bhappy customer\b",
    r"\bclient says\b",
    r"\bpatient says\b",
]


# ==========================================================
# EXTERNAL IMAGE DETECTION
# ==========================================================

EXTERNAL_IMAGE_PATTERNS = [

    r"https?://images\.unsplash\.com/",
    r"https?://source\.unsplash\.com/",
    r"https?://images\.pexels\.com/",
    r"https?://cdn\.pixabay\.com/",
]


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def _normalize(text):

    if not text:

        return ""

    return str(text).lower()


# ==========================================================
# CLAIM DETECTION
# ==========================================================

def _find_matches(text, patterns):

    matches = []

    for pattern in patterns:

        found = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if found:

            for item in found:

                if isinstance(item, tuple):

                    value = " ".join(
                        str(x)
                        for x in item
                        if x
                    )

                else:

                    value = str(item)

                if value.strip():

                    matches.append(
                        value.strip()
                    )

    return matches


# ==========================================================
# WEBSITE OUTPUT VALIDATION
# ==========================================================

def validate_website_output(
    website_output,
    allow_external_images=False,
):

    text = _normalize(
        website_output
    )

    if not text.strip():

        return {

            "valid": False,

            "reason": "Website output is empty.",

            "matches": []

        }

    unsupported_claims = _find_matches(

        text,

        UNSUPPORTED_CLAIM_PATTERNS

    )

    testimonials = _find_matches(

        text,

        TESTIMONIAL_PATTERNS

    )

    external_images = _find_matches(

        text,

        EXTERNAL_IMAGE_PATTERNS

    )

    # ------------------------------------------------------
    # Remove duplicate matches
    # ------------------------------------------------------

    unsupported_claims = list(
        dict.fromkeys(
            unsupported_claims
        )
    )

    testimonials = list(
        dict.fromkeys(
            testimonials
        )
    )

    external_images = list(
        dict.fromkeys(
            external_images
        )
    )

    # ------------------------------------------------------
    # Decide validation result
    # ------------------------------------------------------

    if unsupported_claims:

        return {

            "valid": False,

            "reason": (
                "Potential unsupported business claims "
                "detected in website output."
            ),

            "matches": unsupported_claims

        }

    if testimonials:

        return {

            "valid": False,

            "reason": (
                "Potential testimonials or review claims "
                "detected. Real customer evidence is required."
            ),

            "matches": testimonials

        }

    if external_images and not allow_external_images:

        return {

            "valid": False,

            "reason": (
                "External image URLs detected. "
                "Use approved/local assets instead."
            ),

            "matches": external_images

        }

    return {

        "valid": True,

        "reason": (
            "Website output passed guardrail."
        ),

        "matches": []

    }


# ==========================================================
# BUSINESS-AWARE VALIDATION
# ==========================================================

def validate_website_for_business(

    website_output,

    business_name,

    business_type,

    audience="",

    location="",

    allow_external_images=False,

):

    result = validate_website_output(

        website_output,

        allow_external_images=allow_external_images

    )

    if not result["valid"]:

        return result

    text = _normalize(
        website_output
    )

    # ------------------------------------------------------
    # Business name should normally appear.
    # ------------------------------------------------------

    if business_name:

        if _normalize(
            business_name
        ) not in text:

            return {

                "valid": False,

                "reason": (
                    "Business name was not found "
                    "in generated website."
                ),

                "matches": []

            }

    # ------------------------------------------------------
    # Industry should normally influence the website.
    # ------------------------------------------------------

    if business_type:

        industry_words = [

            word

            for word in re.findall(

                r"[a-zA-Z]+",

                business_type.lower()

            )

            if len(word) > 3

        ]

        if industry_words:

            industry_found = any(

                word in text

                for word in industry_words

            )

            if not industry_found:

                return {

                    "valid": False,

                    "reason": (
                        "Generated website does not appear "
                        "to reflect the supplied business type."
                    ),

                    "matches": []

                }

    return {

        "valid": True,

        "reason": (
            "Website passed business-aware guardrail."
        ),

        "matches": []

    }