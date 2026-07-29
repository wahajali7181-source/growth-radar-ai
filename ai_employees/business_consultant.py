import streamlit as st

from business_ai.consultant_engine import analyze_business


def show():

    st.title("🧠 AI Business Consultant")

    st.caption(
        "Analyze any business and receive AI growth recommendations."
    )

    st.divider()

    business_data = st.session_state.get(
        "selected_business"
    )

    if business_data:

        st.success(
            "Business loaded from Business Finder ✅"
        )

        business_name = business_data.get(
            "name",
            ""
        )

        industry = business_data.get(
            "business_type",
            "Other"
        )

        website = business_data.get(
            "website",
            ""
        )

        location = business_data.get(
            "city",
            ""
        )

    else:

        st.warning(
            "No business selected.\nGo to Business Finder first."
        )

        business_name = st.text_input(
            "Business Name"
        )

        industry = st.selectbox(

            "Industry",

            [

                "Dentist",
                "Real Estate",
                "Restaurant",
                "Gym",
                "Medical",
                "Construction",
                "Education",
                "Law Firm",
                "Ecommerce",
                "Other"

            ]

        )

        website = st.text_input(
            "Website"
        )

        location = st.text_input(
            "Location"
        )

    st.divider()

    if st.button(
        "🚀 Analyze Business",
        use_container_width=True
    ):

        result = analyze_business(

            business_name,
            industry,
            website,
            location

        )

        st.metric(
            "Business Health",
            f"{result['health']}%"
        )

        st.subheader("Strengths")

        for item in result["strengths"]:

            st.success(item)

        st.subheader("Weaknesses")

        for item in result["weaknesses"]:

            st.error(item)

        st.subheader("Recommended Services")

        for item in result["services"]:

            st.info(item)

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Revenue Potential",
            result["revenue"]
        )

        c2.metric(
            "Priority",
            result["priority"]
        )

        c3.metric(
            "Closing Chance",
            f"{result['closing']}%"
        )

        st.session_state["consultant_result"] = result