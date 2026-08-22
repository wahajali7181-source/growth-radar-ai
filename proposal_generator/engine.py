from datetime import datetime

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

IMPORTANT:
Do not invent business facts, traffic, rankings, leads,
reviews, revenue, competitor activity, advertising results,
or ROI.

If information is unavailable, describe it as:
- To be audited
- Recommended action
- Opportunity to investigate
- Potential improvement

Return clean Markdown only.
"""

    ai_summary = ask_ai(
        prompt=prompt,
        system_prompt="""
You are a senior international business growth consultant
working inside Growth Radar AI.

Create a premium, client-facing business proposal using ONLY
the information supplied.

QUALITY RULES:

1. Never invent business facts.
2. Never claim specific traffic, rankings, leads, conversions,
   reviews, ratings, competitor activity, advertising performance,
   revenue, or ROI unless explicitly provided.
3. Treat unavailable information as something to audit or investigate.
4. Never guarantee rankings, leads, revenue, ROI, or specific results.
5. Explain expected outcomes as potential business impact unless
   reliable numerical data is provided.
6. Make recommendations specific to the business, industry, location,
   website, budget, and recommended services.
7. Avoid generic filler.
8. Explain recommendations using WHAT → WHY → BUSINESS IMPACT.
9. Keep the proposal professional, persuasive, and realistic.
10. Write for a real client who may pay for the services.
11. Do not mention that you are an AI.
12. Do not mention demo mode, API limitations, credits, or internal
    Growth Radar AI implementation details.
13. Return ONLY clean Markdown.
14. Do not wrap the entire response inside a markdown code fence.
""",
    )

    if not ai_summary:
        ai_summary = (
            "## Executive Summary\n\n"
            "A detailed business analysis should be completed "
            "before making specific performance claims."
        )

    proposal = PROPOSAL_TEMPLATE.format(
        proposal_date=datetime.now().strftime("%B %d, %Y"),
        business=business,
        industry=industry,
        website=website if website else "Not Available",
        location=location,
        business_summary=ai_summary,
        services=service_text,
        project_value=budget,
    )

    return proposal