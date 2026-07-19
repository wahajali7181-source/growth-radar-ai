import streamlit as st

from lead_engine.collector import collect_businesses
from lead_engine.database import save_businesses

from lead_score.engine import (
    calculate_lead_score,
    opportunity_level
)


def show():

    st.title("🔍 Business Finder")

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

    if st.button("Find Businesses", key="find_businesses"):

        if not business_type or not city:

            st.warning("Please enter Business Type and City.")
            return

        with st.spinner("Finding Businesses..."):

            df = collect_businesses(
                business_type,
                city
            )

        if df.empty:

            st.warning("No businesses found.")
            return

        # ===========================
        # Lead Score
        # ===========================

        scores = []
        opportunities = []

        for _, row in df.iterrows():

            score = calculate_lead_score(row)

            level = opportunity_level(score)

            scores.append(score)
            opportunities.append(level)

        df["lead_score"] = scores
        df["opportunity"] = opportunities

        # ===========================
        # Required Columns
        # ===========================

        if "phone" not in df.columns:
            df["phone"] = ""

        if "address" not in df.columns:
            df["address"] = ""

        df["city"] = city
        df["business_type"] = business_type

        # ===========================
        # DEBUG
        # ===========================

        st.subheader("Debug")

        st.write(df.columns.tolist())

        st.dataframe(df.head())

        # ===========================
        # SAVE
        # ===========================

        try:

            save_businesses(df)

            st.success("Businesses saved to database successfully.")

        except Exception as e:

            st.error(f"Database Error : {e}")

        # ===========================

        st.success(f"Found {len(df)} businesses")

        st.dataframe(
            df,
            use_container_width=True
        )