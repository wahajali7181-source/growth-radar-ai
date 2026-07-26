import streamlit as st

from ai_employees.ai_client import generate_response


def show():

    st.subheader("📄 AI Proposal Writer")

    client_name = st.text_input(
        "Client Name"
    )

    business = st.text_input(
        "Business Type"
    )

    services = st.multiselect(

        "Services",

        [

            "Meta Ads",

            "Google Ads",

            "SEO",

            "Website",

            "Video Editing",

            "Graphic Design",

            "Social Media Management",

            "AI Automation"

        ]

    )

    budget = st.text_input(
        "Monthly Budget ($)"
    )

    if st.button("Generate Proposal"):

        if client_name.strip() == "":

            st.warning("Enter client name.")

            return

        prompt = f"""
Create a professional agency proposal.

Client:

{client_name}

Business:

{business}

Services:

{', '.join(services)}

Monthly Budget:

{budget}

Generate:

Executive Summary

Problems

Solutions

Deliverables

Timeline

Pricing

Expected ROI

Why Choose Us

Closing Statement

Use professional formatting.
"""

        with st.spinner("Writing Proposal..."):

            proposal = generate_response(

                prompt=prompt,

                system_prompt="""
You are a professional Digital Marketing Agency Proposal Writer.

Write premium proposals that close clients.

Use markdown formatting.

Never write short answers.
"""

            )

        st.markdown(proposal)