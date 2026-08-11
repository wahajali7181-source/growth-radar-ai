import streamlit as st

from auth.session import current_user


def show_sidebar():

    user = current_user()

    navigation = [

        "🏠 Dashboard",

        "🔍 Business Finder",

        "📋 CRM",

        "🌐 Website Intelligence",

        "📱 Social Intelligence",

        "📈 Trend Intelligence",

        "🤖 AI Employees",

        "📄 Reports",

        "👤 My Account",

        "💳 Upgrade Plan",

        "⚙ Settings"

    ]

    # ==========================
    # ADMIN ONLY
    # ==========================

    if user and user["role"] == "Admin":

        navigation.append(
            "👑 Admin"
        )

    # ==========================
    # INTERNAL NAVIGATION
    # ==========================

    requested_page = st.session_state.pop(
        "requested_page",
        None
    )

    if requested_page in navigation:

        st.session_state[
            "navigation_radio"
        ] = requested_page

    # ==========================
    # SIDEBAR
    # ==========================

    with st.sidebar:

        st.markdown(
            "# 🚀 Growth Radar AI"
        )

        st.caption(
            "Version 1.0 Beta"
        )

        st.divider()

        page = st.radio(

            "Navigation",

            navigation,

            key="navigation_radio"

        )

        st.divider()

        st.info(
            """
Growth Radar AI

AI Powered Business Intelligence Platform

Lead Generation
CRM
Website Intelligence
AI Employees
Website Builder
"""
        )

    return page