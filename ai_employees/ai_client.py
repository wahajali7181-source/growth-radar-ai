from services.ai_service import ask_ai


def generate_response(
    prompt,
    system_prompt="You are an expert AI Business Consultant."
):
    return ask_ai(
        prompt=prompt,
        system_prompt=system_prompt
    )