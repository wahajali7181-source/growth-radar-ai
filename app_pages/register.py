import streamlit as st

from auth.database import create_users_table
from auth.register import register_user


def show():

    create_users_table()

    st.title("📝 Create Account")

    st.caption("Create your Growth Radar AI account")

    st.divider()

    full_name = st.text_input(
        "Full Name",
        key="register_name"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm"
    )

    st.divider()

    if st.button(
        "🚀 Create Account",
        key="register_button",
        use_container_width=True
    ):

        success, message = register_user(
            full_name,
            email,
            password,
            confirm
        )

        if success:

            st.success(message)

        else:

            st.error(message)