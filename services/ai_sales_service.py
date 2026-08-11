from ai_prompts.sales_json_prompt import build_json_prompt
from ai_engine.json_engine import ask_json


SYSTEM_PROMPT = """
You are Growth Radar AI.

You are a world-class AI Sales Consultant.

Return ONLY valid JSON.

Never use markdown.

Never explain anything outside JSON.

The JSON MUST follow the exact structure requested.
"""


def generate_sales_strategy(
    business_name,
    business_type,
    website,
    country,
    target_audience,
    goal,
    budget,
):

    prompt = build_json_prompt(

        business_name=business_name,

        business_type=business_type,

        website=website,

        country=country,

        target_audience=target_audience,

        goal=goal,

        budget=budget,

    )

    result = ask_json(

        prompt=prompt,

        system_prompt=SYSTEM_PROMPT,

    )

    return result