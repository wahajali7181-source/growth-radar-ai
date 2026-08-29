from website_builder.json_generator import generate_website_json
from website_builder.template_engine import build_react_template
from website_builder.project_builder import create_project

from ai_employees.website_guardrail import validate_website_output


def generate_complete_website(
    business_name,
    business_type,
    audience,
    style,
    colors,
    pages,
    cta
):
    """
    Complete Website Builder pipeline.

    Flow:
        JSON Generator
            ↓
        React Template Generator
            ↓
        Website Guardrail
            ↓
        Project Builder
            ↓
        Final Result
    """

    # ==========================================================
    # STEP 1 — GENERATE WEBSITE JSON
    # ==========================================================

    try:

        data = generate_website_json(
            business_name,
            business_type,
            audience,
            style,
            colors,
            pages,
            cta
        )

    except Exception as e:

        return {
            "success": False,
            "folder": None,
            "json": None,
            "react_code": None,
            "guardrail": None,
            "error": f"Website JSON generation failed: {e}",
            "reason": "json_generation_error"
        }

    if data is None:

        return {
            "success": False,
            "folder": None,
            "json": None,
            "react_code": None,
            "guardrail": None,
            "error": "Website JSON generation failed.",
            "reason": "json_generation_failed"
        }

    # ==========================================================
    # STEP 2 — BUILD REACT TEMPLATE
    # ==========================================================

    try:

        react_code = build_react_template(
            data,
            pages 
        )

    except Exception as e:

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": None,
            "guardrail": None,
            "error": f"React website generation failed: {e}",
            "reason": "react_generation_error"
        }

    if not react_code:

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": None,
            "guardrail": None,
            "error": "React website generation returned empty code.",
            "reason": "empty_react_code"
        }

    # ==========================================================
    # STEP 3 — WEBSITE GUARDRAIL
    # ==========================================================

    try:

        guardrail = validate_website_output(
            react_code
        )

    except Exception as e:

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": react_code,
            "guardrail": None,
            "error": f"Website guardrail failed: {e}",
            "reason": "guardrail_error"
        }

    if not guardrail.get("valid", False):

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": react_code,
            "guardrail": guardrail,
            "error": (
                "Website output failed the "
                "business-claim guardrail."
            ),
            "reason": "guardrail_failed"
        }

    # ==========================================================
    # STEP 4 — CREATE PROJECT
    # ==========================================================

    try:

        folder = create_project(
            business_name,
            react_code
        )

    except Exception as e:

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": react_code,
            "guardrail": guardrail,
            "error": f"Website project creation failed: {e}",
            "reason": "project_creation_error"
        }

    if not folder:

        return {
            "success": False,
            "folder": None,
            "json": data,
            "react_code": react_code,
            "guardrail": guardrail,
            "error": "Website project folder was not created.",
            "reason": "project_creation_failed"
        }

    # ==========================================================
    # STEP 5 — SUCCESS
    # ==========================================================

    return {
        "success": True,
        "folder": folder,
        "json": data,
        "react_code": react_code,
        "guardrail": guardrail,
        "error": None,
        "reason": None
    }