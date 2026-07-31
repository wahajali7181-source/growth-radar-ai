import streamlit as st

from auth.session import require_auth
def show():
    require_auth()

    st.title("🌐 Website Intelligence")

    st.title("⚙ Settings")

    st.info("Settings module coming soon.")