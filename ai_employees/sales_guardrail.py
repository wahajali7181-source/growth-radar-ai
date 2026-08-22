import re


# ==========================================================
# SALES OUTPUT GUARDRAIL
# ==========================================================

FORBIDDEN_PATTERNS = [

    # Unsupported percentages
    r"\b\d+(?:\.\d+)?\s*%\b",

    # Multipliers such as 2x, 3x
    r"\b\d+(?:\.\d+)?\s*x\b",

    # Money claims
    r"\$\s*\d+(?:,\d{3})*(?:\.\d+)?",

    # Lead / appointment / revenue numerical claims
    r"\b\d+(?:,\d{3})*\+?\s*(?:leads?|appointments?|bookings?|customers?|patients?)\b",

    r"\b(?:increase|decrease|reduce|improve|boost|grow|generate)\b.{0,60}"
    r"\b\d+(?:\.\d+)?\s*%",

    # Rankings
    r"\b(?:#|number\s+one|top\s+\d+|rank(?:ing)?\s+\d+)\b",

    # Fake guarantee language
    r"\b(?:guaranteed|guarantee|will\s+generate|will\s+increase|will\s+double)\b",

    # Fake social proof / case study language
    r"\b(?:our\s+clients?|clients?\s+typically|similar\s+clinics?|"
    r"case\s+stud(?:y|ies)|we\s+have\s+helped)\b",

    # Unsupported statistics
    r"\b\d+(?:\.\d+)?\s*(?:million|billion|thousand)\b",
]


def find_suspicious_claims(text):

    if not text:
        return []

    matches = []

    for pattern in FORBIDDEN_PATTERNS:

        found = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        matches.extend(found)

    return matches


def validate_sales_output(text):

    suspicious = find_suspicious_claims(text)

    if suspicious:

        return {
            "valid": False,
            "reason": (
                "Potential unsupported numerical or factual "
                "claims detected."
            ),
            "matches": suspicious,
        }

    return {
        "valid": True,
        "reason": "Sales output passed guardrail.",
        "matches": [],
    }


def clean_markdown_wrapper(text):

    if not text:
        return text

    text = text.strip()

    if text.startswith("```markdown"):

        text = text[len("```markdown"):].strip()

    if text.endswith("```"):

        text = text[:-3].strip()

    return text