import streamlit as st

from ai.widgets.business_selector import show as business_selector

from ai_employees.prompt_builder import build_sales_prompt
from ai_employees.ai_client import generate_response


def show():

    st.title("💼 AI Sales Consultant")

    st.caption(
        "Analyze businesses and generate professional sales strategies."
    )

    st.divider()

    business = business_selector()

    if business is None:

        return

    st.divider()

    if st.button(

        "🚀 Generate Sales Strategy",

        use_container_width=True

    ):

        prompt = build_sales_prompt(

            business_name=business.name,

            business_type=business.business_type,

            website=business.website

        )

        with st.spinner(

            "AI Sales Consultant is thinking..."

        ):

            strategy = generate_response(

                prompt=prompt,

                system_prompt="""
You are Growth Radar AI.

You are a Senior B2B Sales Consultant.

Generate a complete sales strategy.

Include:

# Executive Summary

# Biggest Opportunities

# Lead Generation

# Outreach Strategy

# Closing Strategy

# Recommended Services

# 30-Day Action Plan

Always explain WHY.

Always give actionable advice.

Always use markdown.
"""

            )

        st.success(

            "Sales Strategy Generated"

        )

        st.markdown(strategy)