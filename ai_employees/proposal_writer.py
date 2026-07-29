import streamlit as st

from proposal_generator.engine import generate_proposal
from proposal_generator.pdf import generate_pdf

def show():

    st.title("📄 AI Proposal Writer")

    st.caption(
        "Generate professional proposals for your clients."
    )

    st.divider()

    # ==========================================
    # Load Business From Session
    # ==========================================

    business_data = st.session_state.get(
        "selected_business"
    )

    consultant = st.session_state.get(
        "consultant_result"
    )

    if business_data:

        st.success(
            "Business loaded automatically ✅"
        )

        business = business_data.get(
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

        st.write(f"**Business:** {business}")
        st.write(f"**Industry:** {industry}")
        st.write(f"**Website:** {website if website else 'Not Available'}")
        st.write(f"**Location:** {location}")

    else:

        business = st.text_input(
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
            "Website (Optional)"
        )

        location = st.text_input(
            "Location"
        )

    # ==========================================
    # Services
    # ==========================================

    default_services = []

    if consultant:

        default_services = consultant.get(
            "services",
            []
        )

        st.subheader("🤖 AI Recommended Services")

        for service in default_services:

            st.success(service)

    services = st.multiselect(

        "Services",

        [

            "Website Development",
            "SEO",
            "Local SEO",
            "Google Ads",
            "Meta Ads",
            "Social Media Management",
            "Video Editing",
            "Graphic Designing",
            "Lead Generation"

        ],

        default=default_services

    )

    budget = st.selectbox(

        "Estimated Budget",

        [

            "$500",
            "$1000",
            "$2000",
            "$5000",
            "Custom"

        ]

    )

    st.divider()

    # ==========================================
    # Generate Proposal
    # ==========================================

    if st.button(

        "🚀 Generate Proposal",

        use_container_width=True

    ):

        if not business:

            st.warning(
                "Please enter business name."
            )

            return

        proposal = generate_proposal(

            business,
            industry,
            website,
            location,
            budget

        )

        st.subheader("📄 Proposal")

        st.text_area(

            "",

            proposal,

            height=650

        )
        pdf = generate_pdf(proposal)

        st.download_button(

            "📄 Download Proposal PDF",

            data=pdf,

            file_name=f"{business}_Proposal.pdf",

            mime="application/pdf",

            use_container_width=True

)