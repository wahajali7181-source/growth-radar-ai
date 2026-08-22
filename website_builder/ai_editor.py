import json
import re

from website_builder.json_generator import (
    generate_response
)


# ==========================================================
# AI WEBSITE EDITOR PLANNER
# ==========================================================

ALLOWED_OPERATIONS = {

    "replace_text",
    "append_css"

}


# ==========================================================
# CLEAN AI RESPONSE
# ==========================================================

def _clean_json_response(
    response
):

    if not response:

        return None

    text = str(
        response
    ).strip()

    if text.startswith(
        "```"
    ):

        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

        text = text.strip()

    return text


# ==========================================================
# VALIDATE EDIT PLAN
# ==========================================================

def validate_edit_plan(
    plan
):

    if not isinstance(
        plan,
        dict
    ):

        return {

            "success": False,

            "message":
                "AI did not return a valid edit plan."

        }

    operation = str(
        plan.get(
            "operation",
            ""
        )
    ).strip().lower()

    if operation not in ALLOWED_OPERATIONS:

        return {

            "success": False,

            "message":
                f"Unsupported edit operation: {operation}"

        }

    # ------------------------------------------------------
    # REPLACE TEXT
    # ------------------------------------------------------

    if operation == "replace_text":

        old_text = plan.get(
            "old_text"
        )

        new_text = plan.get(
            "new_text"
        )

        if not isinstance(
            old_text,
            str
        ) or not old_text.strip():

            return {

                "success": False,

                "message":
                    "Edit plan is missing old_text."

            }

        if new_text is None:

            new_text = ""

        if not isinstance(
            new_text,
            str
        ):

            return {

                "success": False,

                "message":
                    "Edit plan new_text must be text."

            }

        replace_all = bool(
            plan.get(
                "replace_all",
                False
            )
        )

        return {

            "success": True,

            "plan": {

                "operation":
                    "replace_text",

                "old_text":
                    old_text,

                "new_text":
                    new_text,

                "replace_all":
                    replace_all

            }

        }

    # ------------------------------------------------------
    # APPEND CSS
    # ------------------------------------------------------

    if operation == "append_css":

        css = plan.get(
            "css"
        )

        if not isinstance(
            css,
            str
        ) or not css.strip():

            return {

                "success": False,

                "message":
                    "Edit plan is missing CSS."

            }

        return {

            "success": True,

            "plan": {

                "operation":
                    "append_css",

                "css":
                    css.strip()

            }

        }

    return {

        "success": False,

        "message":
            "Unable to validate edit plan."

    }


# ==========================================================
# GENERATE AI EDIT PLAN
# ==========================================================

def generate_edit_plan(
    instruction
):

    if not instruction:

        return {

            "success": False,

            "message":
                "Edit instruction is required."

        }

    instruction = str(
        instruction
    ).strip()

    if not instruction:

        return {

            "success": False,

            "message":
                "Edit instruction is required."

        }

    prompt = f"""
Convert the following website editing request into
ONE safe JSON edit plan.

USER REQUEST:

{instruction}

ALLOWED OPERATIONS:

1. replace_text

Structure:

{{
    "operation": "replace_text",
    "old_text": "",
    "new_text": "",
    "replace_all": false
}}

Use replace_all true only when the user clearly wants
all matching occurrences changed.

2. append_css

Structure:

{{
    "operation": "append_css",
    "css": ""
}}

RULES:

- Return ONLY valid JSON.
- Do not use Markdown.
- Do not use code fences.
- Do not add explanations.
- Use ONLY one operation.
- Never invent text that the user did not request.
- For text replacement, preserve the user's intended text.
- If the request cannot safely be represented using one
  allowed operation, return:

{{
    "operation": "unsupported"
}}
"""

    try:

        response = generate_response(
            prompt=prompt,
            system_prompt="""
You are a website editing planner.

Your job is to convert user instructions into
one safe JSON edit plan.

Return ONLY valid JSON.

Never return Markdown.

Never return explanations.

Only use allowed operations.
"""
        )

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to generate AI edit plan.",

            "error":
                str(e)

        }

    cleaned = _clean_json_response(
        response
    )

    if not cleaned:

        return {

            "success": False,

            "message":
                "AI returned an empty edit plan."

        }

    try:

        plan = json.loads(
            cleaned
        )

    except Exception as e:

        return {

            "success": False,

            "message":
                "AI returned invalid JSON.",

            "error":
                str(e),

            "raw_response":
                cleaned[:3000]

        }

    validation = validate_edit_plan(
        plan
    )

    if not validation.get(
        "success"
    ):

        return validation

    return {

        "success": True,

        "plan":
            validation.get(
                "plan"
            )

    }
# ==========================================================
# EXECUTE AI WEBSITE EDIT
# ==========================================================

def execute_ai_edit(
    folder,
    instruction
):

    if not folder:

        return {

            "success": False,

            "message":
                "Website folder is missing."

        }

    if not instruction:

        return {

            "success": False,

            "message":
                "Edit instruction is required."

        }

    # ------------------------------------------------------
    # GENERATE AI PLAN
    # ------------------------------------------------------

    planning_result = generate_edit_plan(
        instruction
    )

    if not planning_result.get(
        "success"
    ):

        return {

            "success": False,

            "message":
                planning_result.get(
                    "message",
                    "Unable to understand the edit request."
                ),

            "error":
                planning_result.get(
                    "error"
                )

        }

    plan = planning_result.get(
        "plan"
    )

    if not plan:

        return {

            "success": False,

            "message":
                "AI did not create a valid edit plan."

        }

    # ------------------------------------------------------
    # IMPORT SAFE EDITOR
    # ------------------------------------------------------

    try:

        from website_builder.editor import (
            edit_website
        )

    except Exception as e:

        return {

            "success": False,

            "message":
                "Website editor backend is unavailable.",

            "error":
                str(e)

        }

    # ------------------------------------------------------
    # EXECUTE SAFE OPERATION
    # ------------------------------------------------------

    operation = plan.get(
        "operation"
    )

    try:

        if operation == "replace_text":

            result = edit_website(

                folder,

                "replace_text",

                old_text=plan.get(
                    "old_text"
                ),

                new_text=plan.get(
                    "new_text"
                ),

                replace_all=plan.get(
                    "replace_all",
                    False
                )

            )

        elif operation == "append_css":

            result = edit_website(

                folder,

                "append_css",

                css=plan.get(
                    "css"
                )

            )

        else:

            return {

                "success": False,

                "message":
                    f"Unsupported AI edit operation: {operation}",

                "plan":
                    plan

            }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Website edit execution failed.",

            "error":
                str(e),

            "plan":
                plan

        }

    # ------------------------------------------------------
    # RETURN RESULT WITH PLAN
    # ------------------------------------------------------

    result[
        "plan"
    ] = plan

    return result