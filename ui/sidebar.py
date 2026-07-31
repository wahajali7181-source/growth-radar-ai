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
    # Admin Only
    # ==========================

    if user and user["role"] == "Admin":

        navigation.append("👑 Admin")

    with st.sidebar:

        st.markdown("# 🚀 Growth Radar AI")

        st.caption("Version 1.0 Beta")

        st.divider()

        page = st.radio(

            "Navigation",

            navigation

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