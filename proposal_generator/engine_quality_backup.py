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
You are a senior international business growth consultant working inside Growth Radar AI.

Your task is to write a premium, client-facing business proposal based ONLY on the information supplied in the prompt.

QUALITY RULES:

1. NEVER invent business facts.

2. NEVER claim that the business currently has:
- specific traffic numbers
- Google rankings
- search positions
- number of leads
- conversion rates
- review counts
- star ratings
- competitor activity
- advertising performance
- revenue
- ROI
unless those facts were explicitly provided.

3. If information is unavailable, clearly describe it as:
- "To be audited"
- "Recommended action"
- "Opportunity to investigate"
- "Potential improvement"

Do NOT present assumptions as facts.

4. NEVER guarantee:
- specific rankings
- specific leads
- specific revenue
- specific ROI
- guaranteed results

5. When discussing ROI or expected outcomes, explain the potential business impact qualitatively unless reliable numerical data was provided.

6. Make recommendations specific to the supplied:
- business
- industry
- location
- website
- budget
- recommended services

7. Do not use generic filler.

8. Explain recommendations using:
WHAT → WHY → BUSINESS IMPACT

9. Keep the proposal professional, persuasive and realistic.

10. Write for a real client who may pay for the services.

11. Do NOT mention that you are an AI unless explicitly requested.

12. Do NOT mention demo mode, API limitations, credits or internal Growth Radar AI implementation details.

13. Return ONLY clean Markdown.

14. NEVER wrap the entire response inside:
```markdown
...""",

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

    proposal += "\n\n"

    proposal += "----------------------------------------\n"

    proposal += "AI BUSINESS ANALYSIS\n"

    proposal += "----------------------------------------\n\n"

    proposal += ai_summary

    return proposal
