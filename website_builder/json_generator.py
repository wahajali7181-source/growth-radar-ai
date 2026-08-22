import json
import re

from ai_employees.ai_client import generate_response


def _clean_json_response(response):
    """
    Clean common AI JSON formatting problems.
    """

    if response is None:
        return None

    # Some AI clients may return a non-string object
    if not isinstance(response, str):
        response = str(response)

    response = response.strip()

    if not response:
        return None

    # Remove markdown code fences
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    response = response.strip()

    # Find the outermost JSON object if the model
    # added text before/after the JSON.
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end <= start:
        return None

    response = response[start:end + 1]

    return response.strip()


def _validate_website_data(data):
    """
    Validate the minimum website JSON structure.
    """

    if not isinstance(data, dict):
        return False

    required_keys = [
        "name",
        "industry",
        "hero",
        "about",
        "services",
        "testimonials",
        "faq",
        "colors"
    ]

    for key in required_keys:

        if key not in data:
            return False

    if not isinstance(data["hero"], dict):
        return False

    hero_keys = [
        "title",
        "description",
        "button"
    ]

    for key in hero_keys:

        if key not in data["hero"]:
            return False

    if not isinstance(data["services"], list):
        return False

    if not isinstance(data["testimonials"], list):
        return False

    if not isinstance(data["faq"], list):
        return False

    if not isinstance(data["colors"], dict):
        return False

    return True


def generate_website_json(
    business_name,
    business_type,
    audience,
    style,
    colors,
    pages,
    cta
):

    prompt = f"""
Create the content structure for a professional business website.

Business Name:
{business_name}

Business Type:
{business_type}

Target Audience:
{audience}

Design Style:
{style}

Requested Colors:
{colors}

Requested Pages:
{pages}

Primary CTA:
{cta}

IMPORTANT DATA INTEGRITY RULES:

1. Use ONLY the information supplied above.

2. NEVER invent:
- years of experience
- number of customers
- patient/client numbers
- reviews
- ratings
- awards
- certifications
- guarantees
- revenue
- rankings
- statistics
- testimonials
- business achievements

3. Do not create fake testimonials.

4. The testimonials array MUST be empty unless
actual testimonials were explicitly supplied.

5. If business-specific information is unavailable,
use neutral professional wording.

6. Do not claim that the business is the best,
#1, leading, award-winning, trusted by thousands,
or similar unless explicitly provided.

7. Create useful website content based only on:
business name, business type, audience, style,
colors, pages and CTA.

Return ONLY valid JSON.

DO NOT use Markdown.

DO NOT use a code block.

DO NOT add explanations before or after JSON.

Use exactly this structure:

{{
    "name": "",
    "industry": "",

    "hero": {{
        "title": "",
        "description": "",
        "button": ""
    }},

    "about": "",

    "services": [
        "",
        "",
        ""
    ],

    "testimonials": [],

    "faq": [
        {{
            "question": "",
            "answer": ""
        }}
    ],

    "colors": {{
        "primary": "",
        "secondary": ""
    }}
}}
"""

    try:

        response = generate_response(
            prompt=prompt,
            system_prompt="""
You are a senior website content strategist.

Return ONLY valid JSON.

Rules:

- No Markdown.
- No code fences.
- No explanations.
- No unsupported business claims.
- Never invent testimonials.
- Never invent statistics.
- Never invent business achievements.
- Use neutral wording when information is unavailable.

The response must be valid JSON that can be parsed
directly using Python json.loads().
"""
        )

    except Exception as e:

        print(
            f"[Website JSON Generator] AI request failed: {e}"
        )

        return None

    cleaned = _clean_json_response(response)

    if cleaned is None:

        print(
            "[Website JSON Generator] "
            "AI returned empty or non-JSON output."
        )

        return None

    try:

        data = json.loads(cleaned)

    except json.JSONDecodeError as e:

        print(
            "[Website JSON Generator] "
            f"Invalid JSON returned by AI: {e}"
        )

        print(
            "[Website JSON Generator] "
            f"Raw response: {cleaned[:3000]}"
        )

        return None

    if not _validate_website_data(data):

        print(
            "[Website JSON Generator] "
            "JSON structure validation failed."
        )

        return None

    return data