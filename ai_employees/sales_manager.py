import streamlit as st

from ai_employees.prompt_builder import build_sales_prompt
from ai_employees.ai_client import generate_response


def show():

    st.subheader("💼 AI Sales Manager")

    st.write(
        "Generate a complete AI-powered sales strategy for any business."
    )

    business_name = st.text_input(
        "Business Name"
    )

    business_type = st.text_input(
        "Business Type"
    )

    website = st.text_input(
        "Website"
    )

    if st.button("Generate Sales Strategy"):

        if business_name.strip() == "":

            st.warning("Please enter Business Name.")
            return

        prompt = build_sales_prompt(
            business_name=business_name,
            business_type=business_type,
            website=website
        )

        with st.spinner("🤖 AI Sales Manager is creating strategy..."):

            strategy = generate_response(
                prompt=prompt,
                system_prompt="""
You are a world-class B2B Sales Consultant.

Generate a professional sales strategy with these sections:

1. Business Overview
2. Biggest Opportunities
3. Sales Strategy
4. Lead Generation Plan
5. Outreach Strategy
6. Closing Strategy
7. Recommended Marketing Services
8. 30-Day Action Plan

Write professionally using markdown headings and bullet points.
"""
            )

        st.markdown("## 📈 AI Sales Strategy")

        st.markdown(strategy)