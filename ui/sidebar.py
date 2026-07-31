import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.markdown("# 🚀 Growth Radar AI")

        st.caption("Version 1.0 Beta")

        st.divider()

        page = st.radio(

            "Navigation",

            [

                "🏠 Dashboard",

                "🔍 Business Finder",

                "📋 CRM",

                "🌐 Website Intelligence",


                "📱 Social Intelligence",

                "📈 Trend Intelligence",

                "🤖 AI Employees",

                "📄 Reports",
                 
                "👤 My Account",
                 
                "⚙ Settings"

            ]

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