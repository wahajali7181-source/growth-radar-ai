import streamlit as st

from auth.session import (
    require_auth,
    current_user
)

from subscriptions.engine import (
    has_access,
    get_remaining,
    needs_upgrade
)

from subscriptions.usage import (
    increase_usage
)

from lead_engine.collector import collect_businesses
from lead_engine.database import save_businesses

from lead_score.engine import (
    calculate_lead_score,
    opportunity_level
)

from crm.ui import crm_card


def show():

    # ===================================
    # AUTH
    # ===================================

    require_auth()

    user = current_user()

    email = user["email"]

    # ===================================
    # PAGE
    # ===================================

    st.title("🔍 Business Finder")

    st.caption(
        "Find high quality business leads using AI."
    )

    st.divider()

    # ===================================
    # SUBSCRIPTION
    # ===================================

    remaining = get_remaining(

        email,

        "business_finder"

    )

    col1, col2 = st.columns([3, 1])

    with col1:

        st.info(
            f"Remaining Searches : {remaining}"
        )

    with col2:

        st.button(
            "⭐ Upgrade",
            use_container_width=True
        )

    st.divider()

    # ===================================
    # SEARCH FORM
    # ===================================

    business_type = st.text_input(

        "Business Type",

        placeholder="Dentist, Gym, Restaurant",

        key="business_type"

    )

    city = st.text_input(

        "City",

        placeholder="Lahore",

        key="city"

    )

    # ===================================
    # SEARCH BUTTON
    # ===================================

    if st.button(

        "🚀 Find Businesses",

        use_container_width=True,

        key="find_businesses"

    ):

        # ===============================

        if not business_type or not city:

            st.warning(

                "Please enter Business Type and City."

            )

            return

        # ===============================
        # SUBSCRIPTION LIMIT
        # ===============================

        if needs_upgrade(

            email,

            "business_finder"

        ):

            st.error(

                "⭐ Monthly limit reached."

            )

            st.warning(

                "Upgrade your subscription."

            )

            st.button(

                "🚀 Upgrade Plan",

                use_container_width=True

            )

            return

        # ===============================
        # SEARCH
        # ===============================

        with st.spinner(

            "Finding businesses..."

        ):

            df = collect_businesses(

                business_type,

                city

            )

        if df.empty:

            st.warning(

                "No businesses found."

            )

            return

        # ==================================
        # LEAD SCORE
        # ==================================

        scores = []

        opportunities = []

        for _, row in df.iterrows():

            score = calculate_lead_score(row)

            scores.append(score)

            opportunities.append(

                opportunity_level(score)

            )

        df["lead_score"] = scores

        df["opportunity"] = opportunities
                # ==================================
        # REQUIRED COLUMNS
        # ==================================

        if "phone" not in df.columns:
            df["phone"] = ""

        if "address" not in df.columns:
            df["address"] = ""

        df["city"] = city
        df["business_type"] = business_type

        # ==================================
        # SAVE DATABASE
        # ==================================

        try:

            save_businesses(df)

            # Subscription Usage +1
            increase_usage(
                email,
                "business_finder"
            )

            st.success(
                f"✅ Found {len(df)} businesses"
            )

            st.success(
                "Businesses saved successfully."
            )

        except Exception as e:

            st.error(
                f"Database Error : {e}"
            )

        st.divider()

        # ==================================
        # RESULTS
        # ==================================

        st.subheader("📊 Search Results")

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================
        # AI CONSULTANT
        # ==================================

        st.subheader("🤖 AI Business Consultant")

        selected_business = st.selectbox(

            "Select Business",

            df["name"],

            key="ai_business"

        )

        business = df[
            df["name"] == selected_business
        ].iloc[0]

        st.session_state["selected_business"] = (
            business.to_dict()
        )

        if st.button(

            "Open AI Consultant",

            use_container_width=True

        ):

            st.success(

                "Business loaded successfully."

            )

        st.divider()

        # ==================================
        # CRM
        # ==================================

        st.subheader("📋 CRM")

        selected_business = st.selectbox(

            "CRM Business",

            df["name"],

            key="crm_business"

        )

        business = df[
            df["name"] == selected_business
        ].iloc[0]

        crm_card(business)