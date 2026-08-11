import json
import re

from services.ai_service import ask_ai


def _extract_json(text):

    if not text:
        return None

    text = text.strip()

    # Remove markdown fences
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    # Find first {
    start = text.find("{")

    # Find last }
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    return text[start:end + 1]


def ask_json(

    prompt,

    system_prompt="You are an expert AI Business Consultant."

):

    full_prompt = f"""
Return ONLY valid JSON.

No markdown.

No explanation.

No code block.

Every field must be completed.

Prompt:

{prompt}
"""

    # ============================
    # First Attempt
    # ============================

    response = ask_ai(

        prompt=full_prompt,

        system_prompt=system_prompt,

    )

    cleaned = _extract_json(response)

    if cleaned:

        try:

            data = json.loads(cleaned)

            data["success"] = True

            return data

        except Exception:
            pass

    # ============================
    # Retry
    # ============================

    retry_prompt = f"""
Your previous response was invalid.

Return ONLY VALID JSON.

No markdown.

No explanation.

Prompt:

{prompt}
"""

    response = ask_ai(

        prompt=retry_prompt,

        system_prompt=system_prompt,

        temperature=0.3,

    )

    cleaned = _extract_json(response)

    if cleaned:

        try:

            data = json.loads(cleaned)

            data["success"] = True

            return data

        except Exception:
            pass

    return {

        "success": False,

        "raw_response": response,

        "error": "AI returned invalid JSON."

    }