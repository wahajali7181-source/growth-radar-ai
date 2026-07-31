import streamlit as st

from auth.session import is_logged_in


def require_login():

    if is_logged_in():

        return

    st.error("🔒 Please login first.")

    st.info(
        "Open the Login page from the sidebar to continue."
    )

    st.stop()