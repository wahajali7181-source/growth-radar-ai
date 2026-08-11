import streamlit as st

from services.ai_sales_service import generate_sales_strategy


def show():

    st.title("💼 AI Sales Consultant")

    st.caption(
        "AI Powered Business Growth & Sales Strategy Generator"
    )

    st.divider()

    with st.form("sales_form"):

        col1, col2 = st.columns(2)

        with col1:

            business_name = st.text_input(
                "Business Name"
            )

            business_type = st.text_input(
                "Business Type"
            )

            website = st.text_input(
                "Website"
            )

            country = st.text_input(
                "Country"
            )

        with col2:

            target_audience = st.text_input(
                "Target Audience"
            )

            budget = st.text_input(
                "Monthly Marketing Budget"
            )

            goal = st.text_area(
                "Business Goal",
                height=120
            )

        submitted = st.form_submit_button(
            "🚀 Generate Strategy",
            use_container_width=True
        )

    if not submitted:
        return

    if business_name.strip() == "":
        st.warning("Please enter Business Name.")
        return

    with st.spinner("Generating AI Strategy..."):

        result = generate_sales_strategy(

            business_name,

            business_type,

            website,

            country,

            target_audience,

            goal,

            budget,

        )

    if not result.get("success", True):

        st.error("AI failed to generate valid JSON.")

        st.code(result.get("raw_response", ""))

        return

    st.success("Strategy Generated Successfully")

    st.divider()

    st.metric(
        "Business Score",
        f"{result.get('business_score',0)}/100"
    )

    st.divider()

    st.subheader("Executive Summary")

    st.write(
        result.get("summary","")
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Strengths")

        for item in result.get("strengths",[]):

            st.write("✅", item)

    with col2:

        st.subheader("Weaknesses")

        for item in result.get("weaknesses",[]):

            st.write("⚠️", item)

    st.divider()

    st.subheader("Growth Opportunities")

    for item in result.get("opportunities",[]):

        st.write("🚀", item)

    st.divider()

    st.subheader("Recommended Services")

    for item in result.get("recommended_services",[]):

        st.write("💼", item)

    st.divider()

    st.subheader("Cold Email")

    st.code(

        result.get("cold_email",""),

        language="text"

    )

    st.subheader("LinkedIn Message")

    st.code(

        result.get("linkedin",""),

        language="text"

    )

    st.subheader("WhatsApp Pitch")

    st.code(

        result.get("whatsapp",""),

        language="text"

    )

    st.divider()

    st.subheader("30 Day Action Plan")

    for item in result.get("action_plan",[]):

        st.write("📌", item)

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.button(
            "📄 Export PDF",
            disabled=True,
            use_container_width=True,
        )

    with c2:

        st.button(
            "💾 Save To CRM",
            disabled=True,
            use_container_width=True,
        )

    with c3:

        st.button(
            "📧 Generate Proposal",
            disabled=True,
            use_container_width=True,
        )