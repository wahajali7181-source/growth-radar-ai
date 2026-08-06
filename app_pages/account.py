import streamlit as st

from auth.session import current_user
from auth.session import logout_session


def show():

    user = current_user()

    if not user:

        st.error("No user session found.")
        return

    st.title("👤 My Account")

    st.caption(
        "Manage your Growth Radar AI account"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Plan",
            user["plan"]
        )

    with col2:

        st.metric(
            "Role",
            user["role"]
        )

    st.divider()

    st.subheader("Profile")

    st.text_input(
        "Full Name",
        value=user["name"],
        disabled=True
    )

    st.text_input(
        "Email",
        value=user["email"],
        disabled=True
    )

    st.divider()

    st.subheader("Usage")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Reports",
        "0"
    )

    col2.metric(
        "Website Audits",
        "0"
    )

    col3.metric(
        "Leads",
        "0"
    )

    st.divider()

    st.subheader("Security")

    st.info(
        "Password change feature coming soon."
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_session()

        st.success("Logged out successfully.")

        st.rerun()