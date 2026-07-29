from business_ai.consultant_engine import analyze_business
from proposal_generator.template import PROPOSAL_TEMPLATE


def generate_proposal(

    business,
    industry,
    website,
    location,
    budget

):

    analysis = analyze_business(

        business,
        industry,
        website,
        location

    )

    services = analysis["services"]

    service_text = "\n".join(

        f"• {service}"

        for service in services

    )

    if not service_text:

        service_text = "• Digital Marketing"

    proposal = PROPOSAL_TEMPLATE.format(

        business=business,

        industry=industry,

        website=website if website else "Not Available",

        location=location,

        services=service_text

    )

    return proposal