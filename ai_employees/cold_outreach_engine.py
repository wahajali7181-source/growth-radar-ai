import json


def build_cold_call_prompt(
    business,
    service,
    tone="Professional",
    objective="Book a Meeting",
):
    """
    Build a structured prompt for the AI cold-call agent.
    """

    business_name = business.get("business_name", "the business")
    industry = business.get("industry", "their industry")
    location = business.get("location", "")
    website = business.get("website", "")
    lead_score = business.get("lead_score", 0)

    return f"""
You are a professional B2B sales representative.

You are calling a business owner or decision maker.

BUSINESS INFORMATION

Business name: {business_name}
Industry: {industry}
Location: {location}
Website: {website}
Lead score: {lead_score}

SERVICE BEING OFFERED

{service}

CONVERSATION STYLE

{tone}

PRIMARY OBJECTIVE

{objective}

YOUR JOB

Have a natural professional conversation with the prospect.

Rules:

1. Speak naturally.
2. Never sound like a robotic script.
3. Keep the opening short.
4. Ask relevant questions before pitching heavily.
5. Understand the prospect's current situation.
6. Identify problems or opportunities.
7. Explain the service only when relevant.
8. Never invent information about the business.
9. If you do not know something, say so.
10. Handle objections professionally.
11. Do not pressure the prospect.
12. If the prospect is interested, move toward the objective.
13. If the prospect is busy, offer a suitable callback.
14. If the prospect says no, remain respectful.
15. Never claim guaranteed results.
16. Keep the conversation focused on business value.

Return a structured sales conversation plan containing:

- opening
- discovery_questions
- value_proposition
- objection_handling
- closing
- follow_up
"""


def build_conversation_context(
    business,
    service,
    objective="Book a Meeting",
):
    """
    Creates structured context that can later be passed
    to an AI text or voice provider.
    """

    return {
        "business": {
            "name": business.get(
                "business_name",
                ""
            ),
            "industry": business.get(
                "industry",
                ""
            ),
            "location": business.get(
                "location",
                ""
            ),
            "website": business.get(
                "website",
                ""
            ),
            "phone": business.get(
                "phone",
                ""
            ),
            "email": business.get(
                "email",
                ""
            ),
            "lead_score": business.get(
                "lead_score",
                0
            ),
        },
        "service": service,
        "objective": objective,
    }


def create_agent_instructions(
    business,
    service,
    tone="Professional",
    objective="Book a Meeting",
):
    """
    Final instructions for a future AI text/voice agent.
    """

    prompt = build_cold_call_prompt(
        business=business,
        service=service,
        tone=tone,
        objective=objective,
    )

    context = build_conversation_context(
        business=business,
        service=service,
        objective=objective,
    )

    return {
        "system_prompt": prompt.strip(),
        "context": context,
        "response_format": "natural_conversation",
    }


def validate_agent_config(config):
    """
    Basic validation before sending the configuration
    to an AI provider.
    """

    required = [
        "system_prompt",
        "context",
        "response_format",
    ]

    for key in required:

        if key not in config:
            return False

    return True


def export_agent_config(config):
    """
    Convert configuration to JSON.
    Useful later for logging, testing,
    or sending to an external voice agent.
    """

    if not validate_agent_config(config):
        raise ValueError(
            "Invalid AI agent configuration."
        )

    return json.dumps(
        config,
        indent=2,
        ensure_ascii=False,
    )