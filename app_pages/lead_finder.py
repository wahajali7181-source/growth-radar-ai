import streamlit as st
import pandas as pd

from auth.session import require_auth, current_user

from subscriptions.engine import (
    get_remaining,
    needs_upgrade,
)

from subscriptions.usage import increase_usage

from lead_engine_v2.collector import collect_businesses

from app_pages.components.metrics import show_metrics
from app_pages.components.filters import show_filters
from app_pages.components.tables import show_table
from app_pages.components.export import export_csv
from app_pages.components.actions import show_actions
from app_pages.components.business_card import show_business_card


def show():

    require_auth()

    user = current_user()

    email = user["email"]

    st.title("🔍 Lead Finder PRO")

    st.caption(
        "Find, score and manage high quality business leads."
    )

    st.divider()

    remaining = get_remaining(

        email,

        "business_finder"

    )

    c1, c2 = st.columns([4, 1])

    with c1:

        st.info(

            f"Remaining Searches : {remaining}"

        )

    with c2:

        st.button(

            "⭐ Upgrade",

            use_container_width=True,

        )

    st.divider()

    with st.form("finder"):

        left, right = st.columns(2)

        with left:

            business_type = st.text_input(

                "Business Type",

                placeholder="Dentist"

            )

        with right:

            city = st.text_input(

                "City",

                placeholder="Lahore"

            )

        search = st.form_submit_button(

            "🚀 Find Businesses",

            use_container_width=True,

        )

    if not search:

        return

    if business_type.strip() == "" or city.strip() == "":

        st.warning(

            "Business Type and City required."

        )

        return

    if needs_upgrade(

        email,

        "business_finder"

    ):

        st.error(

            "Monthly search limit reached."

        )

        return

    with st.spinner(

        "Finding businesses..."

    ):

        df = collect_businesses(

            business_type,

            city,

        )
    if df.empty:

        st.warning(

            "No businesses found."

        )

        return

    increase_usage(

        email,

        "business_finder"

    )

    st.success(

        f"{len(df)} businesses found."

    )

    st.divider()

    # ===========================
    # Dashboard Metrics
    # ===========================

    show_metrics(df)

    st.divider()

    # ===========================
    # Filters
    # ===========================

    filtered = show_filters(df)

    st.divider()

    # ===========================
    # Export
    # ===========================

    export_csv(filtered)

    st.divider()

    # ===========================
    # Results Table
    # ===========================

    st.subheader("📊 Search Results")

    show_table(filtered)

    st.divider()

    # ===========================
    # Business Cards
    # ===========================

    st.subheader("🏢 Business Details")

    for _, business in filtered.iterrows():

        show_business_card(

            business

        )

    st.divider()

    # ===========================
    # Bulk Actions
    # ===========================

    show_actions(filtered)          