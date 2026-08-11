import streamlit as st
import pandas as pd

from auth.session import (
    require_auth,
    current_user
)

from subscriptions.engine import (
    get_remaining,
    needs_upgrade
)

from subscriptions.usage import (
    increase_usage
)

from lead_engine.collector import (
    collect_businesses
)

from lead_engine.database import (
    save_businesses
)

from lead_score.engine import (
    calculate_lead_score,
    opportunity_level
)

from crm.ui import crm_card


def show():

    # ==========================================================
    # AUTH
    # ==========================================================

    require_auth()

    user = current_user()

    if not user:

        st.error(
            "Unable to load user session."
        )

        return

    email = user.get(
        "email",
        ""
    )

    # ==========================================================
    # PAGE HEADER
    # ==========================================================

    st.title(
        "🔍 Business Finder"
    )

    st.caption(
        "Find high-quality business leads using Growth Radar AI."
    )

    st.divider()

    # ==========================================================
    # SUBSCRIPTION USAGE
    # ==========================================================

    remaining = get_remaining(
        email,
        "business_finder"
    )

    col1, col2 = st.columns(
        [3, 1]
    )

    with col1:

        if remaining == "Unlimited":

            st.success(
                "🚀 Business Searches: Unlimited"
            )

        else:

            st.info(
                f"🔎 Remaining Searches: {remaining}"
            )

    with col2:

        if st.button(
            "⭐ Upgrade",
            use_container_width=True,
            key="finder_upgrade_top"
        ):

            st.session_state[
                "requested_page"
            ] = "💳 Upgrade Plan"

            st.rerun()

    st.divider()

    # ==========================================================
    # SEARCH FORM
    # ==========================================================

    st.subheader(
        "🎯 Find New Businesses"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        business_type = st.text_input(
            "Business Type",
            placeholder="Dentist, Gym, Restaurant...",
            key="finder_business_type"
        )

    with col2:

        city = st.text_input(
            "City",
            placeholder="Lahore, Karachi, Dubai...",
            key="finder_city"
        )

    st.caption(
        "Example: Dentist + Lahore"
    )

    st.divider()

    # ==========================================================
    # SEARCH BUTTON
    # ==========================================================

    search_clicked = st.button(
        "🚀 Find Businesses",
        use_container_width=True,
        key="find_businesses"
    )

    if not search_clicked:

        return

    # ==========================================================
    # VALIDATION
    # ==========================================================

    if not business_type.strip():

        st.warning(
            "⚠️ Please enter a Business Type."
        )

        return

    if not city.strip():

        st.warning(
            "⚠️ Please enter a City."
        )

        return

    # ==========================================================
    # SUBSCRIPTION LIMIT
    # ==========================================================

    if needs_upgrade(
        email,
        "business_finder"
    ):

        st.error(
            "🚫 Your monthly Business Finder limit has been reached."
        )

        st.info(
            "Upgrade your plan to continue finding new businesses."
        )

        if st.button(
            "🚀 Upgrade Plan",
            use_container_width=True,
            key="finder_upgrade_limit"
        ):

            st.session_state[
                "requested_page"
            ] = "💳 Upgrade Plan"

            st.rerun()

        return

    # ==========================================================
    # BUSINESS SEARCH
    # ==========================================================

    with st.spinner(
        "🤖 Finding businesses..."
    ):

        try:

            df = collect_businesses(
                business_type.strip(),
                city.strip()
            )

        except Exception as e:

            st.error(
                f"❌ Business Finder Error: {e}"
            )

            return

    # ==========================================================
    # EMPTY RESULTS
    # ==========================================================

    if df is None or df.empty:

        st.warning(
            "No businesses were found for this search."
        )

        return

    # ==========================================================
    # COPY DATAFRAME
    # ==========================================================

    df = df.copy()

    # ==========================================================
    # REQUIRED COLUMNS
    # ==========================================================

    required_columns = {

        "name": "",

        "phone": "",

        "address": "",

        "website": "",

        "email": ""

    }

    for column, default in required_columns.items():

        if column not in df.columns:

            df[column] = default

    # ==========================================================
    # SEARCH INFORMATION
    # ==========================================================

    df["city"] = city.strip()

    df["business_type"] = (
        business_type.strip()
    )

    # ==========================================================
    # LEAD SCORING
    # ==========================================================

    scores = []

    opportunities = []

    for _, row in df.iterrows():

        try:

            score = calculate_lead_score(
                row
            )

        except Exception:

            score = 0

        try:

            opportunity = opportunity_level(
                score
            )

        except Exception:

            opportunity = "Unknown"

        scores.append(
            score
        )

        opportunities.append(
            opportunity
        )

    df["lead_score"] = scores

    df["opportunity"] = opportunities

    # ==========================================================
    # SORT BY LEAD SCORE
    # ==========================================================

    if "lead_score" in df.columns:

        df = df.sort_values(
            "lead_score",
            ascending=False
        ).reset_index(
            drop=True
        )

    # ==========================================================
    # SAVE TO DATABASE
    # ==========================================================

    try:

        save_businesses(
            df
        )

    except Exception as e:

        st.error(
            f"❌ Database Error: {e}"
        )

        return

    # ==========================================================
    # INCREASE SUBSCRIPTION USAGE
    # ==========================================================

    try:

        increase_usage(
            email,
            "business_finder"
        )

    except Exception as e:

        st.warning(
            f"Search completed, but usage tracking failed: {e}"
        )

    # ==========================================================
    # SUCCESS
    # ==========================================================

    st.success(
        f"✅ Found {len(df)} businesses successfully."
    )

    st.caption(
        "Businesses have been saved to your lead database."
    )

    # ==========================================================
    # RESULTS
    # ==========================================================

    st.divider()

    st.subheader(
        "📊 Search Results"
    )

    # ==========================================================
    # QUICK STATS
    # ==========================================================

    total_results = len(df)

    high_priority = 0

    medium_priority = 0

    low_priority = 0

    if "opportunity" in df.columns:

        opportunity_text = (
            df["opportunity"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        high_priority = opportunity_text.str.contains(
            "high",
            na=False
        ).sum()

        medium_priority = opportunity_text.str.contains(
            "medium",
            na=False
        ).sum()

        low_priority = opportunity_text.str.contains(
            "low",
            na=False
        ).sum()

    c1, c2, c3, c4 = st.columns(
        4
    )

    c1.metric(
        "Businesses",
        total_results
    )

    c2.metric(
        "🔥 High Opportunity",
        high_priority
    )

    c3.metric(
        "🟡 Medium",
        medium_priority
    )

    c4.metric(
        "🟢 Low",
        low_priority
    )

    st.divider()

    # ==========================================================
    # DATA TABLE
    # ==========================================================

    display_columns = [

        "name",

        "business_type",

        "city",

        "phone",

        "website",

        "lead_score",

        "opportunity"

    ]

    available_columns = [

        column

        for column in display_columns

        if column in df.columns

    ]

    if available_columns:

        st.dataframe(

            df[
                available_columns
            ],

            use_container_width=True,

            hide_index=True

        )

    else:

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

    # ==========================================================
    # AI BUSINESS CONSULTANT
    # ==========================================================

    st.divider()

    st.subheader(
        "🤖 AI Business Consultant"
    )

    st.caption(
        "Select a business to analyze its growth opportunities."
    )

    if "name" not in df.columns:

        st.warning(
            "Business names are not available."
        )

        return

    business_names = (

        df["name"]
        .fillna("")
        .astype(str)
        .tolist()

    )

    business_names = [

        name

        for name in business_names

        if name.strip()

    ]

    if not business_names:

        st.info(
            "No businesses available for analysis."
        )

        return

    selected_business_name = st.selectbox(

        "Select Business",

        business_names,

        key="ai_business"

    )

    selected_business = df[
        df["name"]
        .astype(str)
        == selected_business_name
    ].iloc[0]

    st.session_state[
        "selected_business"
    ] = selected_business.to_dict()

    if st.button(

        "🧠 Open AI Consultant",

        use_container_width=True,

        key="open_ai_consultant"

    ):

        st.session_state[
            "selected_business"
        ] = selected_business.to_dict()

        st.success(
            "✅ Business loaded into AI Consultant."
        )

        st.info(
            "Open AI Employees from the sidebar to continue the analysis."
        )

    # ==========================================================
    # CRM
    # ==========================================================

    st.divider()

    st.subheader(
        "📋 CRM"
    )

    st.caption(
        "Add the selected business to your CRM pipeline."
    )

    crm_card(
        selected_business
    )