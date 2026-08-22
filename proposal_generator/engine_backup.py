from business_ai.consultant_engine import analyze_business
from proposal_generator.template import PROPOSAL_TEMPLATE
from services.ai_service import ask_ai


def generate_proposal(

    business,
    industry,
    website,
    location,
    budget,

):

    analysis = analyze_business(

        business,
        industry,
        website,
        location,

    )

    services = analysis.get("services", [])

    if not services:

        services = [
            "Digital Marketing",
            "SEO",
            "Meta Ads",
        ]

    service_text = "\n".join(

        f"• {service}"

        for service in services

    )

    # ----------------------------------
    # AI Executive Summary
    # ----------------------------------

    prompt = f"""
Business:
{business}

Industry:
{industry}

Website:
{website}

Location:
{location}

Monthly Budget:
{budget}

Recommended Services:
{service_text}

Write:

1. Executive Summary

2. Current Business Situation

3. Main Growth Opportunities

4. Expected ROI

Professional tone.
"""

    ai_summary = ask_ai(

        prompt=prompt,

        system_prompt="""
You are a senior business consultant.

Write concise, premium-quality business proposals.

Never use generic advice.

Return markdown only.
""",

    )

    proposal = PROPOSAL_TEMPLATE.format(

        business=business,

        industry=industry,

        website=website if website else "Not Available",

        location=location,

        services=service_text,

    )

    proposal += "\n\n"

    proposal += "----------------------------------------\n"

    proposal += "AI BUSINESS ANALYSIS\n"

    proposal += "----------------------------------------\n\n"

    proposal += ai_summary

    return proposal