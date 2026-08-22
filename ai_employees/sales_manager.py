import streamlit as st

from ai.widgets.business_selector import show as business_selector

from ai_employees.prompt_builder import build_sales_prompt
from ai_employees.ai_client import generate_response
from ai_employees.sales_guardrail import (
    validate_sales_output,
    clean_markdown_wrapper,
)


def show():

    st.title("💼 AI Sales Consultant")

    st.caption(
        "Analyze businesses and generate professional sales strategies."
    )

    st.divider()

    # ==========================================================
    # BUSINESS SELECTOR
    # ==========================================================

    business = business_selector()

    if business is None:
        return

    st.divider()

    # ==========================================================
    # GENERATE SALES STRATEGY
    # ==========================================================

    if st.button(
        "🚀 Generate Sales Strategy",
        use_container_width=True,
    ):

        # ------------------------------------------------------
        # Build prompt using complete business intelligence
        # ------------------------------------------------------

        prompt = build_sales_prompt(

            business_name=business.name,

            business_type=business.business_type,

            website=business.website,

            country=getattr(
                business,
                "country",
                "",
            ),

            target_audience=getattr(
                business,
                "target_audience",
                "",
            ),

            goal=getattr(
                business,
                "goal",
                "Generate More Leads",
            ),

            budget=getattr(
                business,
                "budget",
                "",
            ),

            city=getattr(
                business,
                "city",
                "",
            ),

            lead_score=getattr(
                business,
                "lead_score",
                None,
            ),

            priority=getattr(
                business,
                "priority",
                "",
            ),

            crm_status=getattr(
                business,
                "status",
                "",
            ),

            deal_stage=getattr(
                business,
                "deal_stage",
                "",
            ),

            notes=getattr(
                business,
                "notes",
                "",
            ),

        )

        # ======================================================
        # AI GENERATION
        # ======================================================

        system_prompt = """
You are an elite international B2B Sales Manager.

You work inside Growth Radar AI.

Create practical, professional and realistic sales strategies.

STRICT DATA RULES:

- Never invent business facts.
- Never invent statistics.
- Never invent percentages.
- Never invent revenue.
- Never invent lead numbers.
- Never invent conversion rates.
- Never invent rankings.
- Never invent reviews.
- Never invent competitors.
- Never invent testimonials.
- Never invent case studies.
- Never guarantee results.
- Never claim a specific ROI unless explicitly supplied.
- Never claim previous client results unless explicitly supplied.

If information is unavailable, clearly say:

Requires Audit
To Be Investigated
Potential Opportunity
Recommended Action

Treat Lead Score as an internal lead-priority signal only.

Do not interpret Lead Score as revenue, conversion probability,
sales performance or guaranteed purchase intent.

Use clean Markdown.

Do not mention AI implementation details.
"""

        with st.spinner(
            "🤖 AI Sales Consultant is analyzing the business..."
        ):

            result = generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
            )

        # ======================================================
        # HANDLE AI RESPONSE
        # ======================================================

        if isinstance(result, dict):

            if not result.get("success"):

                st.error(
                    f"❌ AI Error: "
                    f"{result.get('error', 'Unknown error')}"
                )

                return

            strategy = result.get(
                "response",
                "",
            )

        else:

            strategy = result

        if not strategy:

            st.error(
                "❌ AI returned an empty response."
            )

            return

        # ======================================================
        # CLEAN MARKDOWN WRAPPER
        # ======================================================

        strategy = clean_markdown_wrapper(
            strategy
        )

        # ======================================================
        # SALES GUARDRAIL
        # ======================================================

        validation = validate_sales_output(
            strategy
        )

        # ======================================================
        # BLOCK UNSUPPORTED CLAIMS
        # ======================================================

        if not validation["valid"]:

            st.warning(
                "⚠️ AI output failed the Sales Quality Guardrail."
            )

            st.error(
                "The generated strategy contains potentially "
                "unsupported numerical or factual claims."
            )

            with st.expander(
                "🔍 Guardrail Details"
            ):

                st.write(
                    validation["matches"]
                )

            st.info(
                "Please generate the strategy again. "
                "The report was not displayed because "
                "Growth Radar AI protects against unsupported claims."
            )

            return

        # ======================================================
        # SAVE VERIFIED RESULT
        # ======================================================

        st.session_state[
            "sales_strategy"
        ] = strategy

        st.session_state[
            "sales_strategy_business"
        ] = business.name

        # ======================================================
        # SUCCESS
        # ======================================================

        st.success(
            "✅ Sales Strategy Generated & Verified"
        )

        st.markdown(
            strategy
        )

    # ==========================================================
    # DISPLAY PREVIOUS VERIFIED RESULT
    # ==========================================================

    saved_strategy = st.session_state.get(
        "sales_strategy"
    )

    saved_business = st.session_state.get(
        "sales_strategy_business",
        "",
    )

    if saved_strategy:

        st.divider()

        st.subheader(
            f"📋 Sales Strategy — {saved_business}"
        )

        st.markdown(
            saved_strategy
        )

        st.download_button(
            "📥 Download Sales Strategy",
            data=saved_strategy,
            file_name=(
                f"{saved_business}_sales_strategy.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )