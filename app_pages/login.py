import streamlit as st

from auth.login import login_user
from auth.session import login_session


def show():

    st.title("🔐 Login")

    st.caption("Login to Growth Radar AI")

    st.divider()

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    st.divider()

    if st.button(
        "🚀 Login",
        key="login_button",
        use_container_width=True
    ):

        success, result = login_user(
            email,
            password
        )

        if success:

            login_session(result)

            st.success(
                f"Welcome back, {result['name']}!"
            )

            st.rerun()

        else:

            st.error(result)