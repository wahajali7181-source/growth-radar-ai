import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.markdown("# 🚀 Growth Radar AI")

        st.caption("Version 0.5 Beta")

        st.divider()

        page = st.radio(

            "Navigation",

            [

                "🏠 Dashboard",

                "🔍 Business Finder",

                "🌐 Website Intelligence",

                "📱 Social Intelligence",

                "📈 Trend Intelligence",

                "📄 Reports",

                "⚙ Settings"

            ]

        )

        st.divider()

        st.info(

            "Growth Radar AI\n\nAI Powered Business Intelligence Platform"

        )

    return page