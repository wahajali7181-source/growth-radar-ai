import streamlit as st
from auth.login import login_user, register_user


def require_login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return

    st.title("🔐 Growth Radar AI Login")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login_user(email, password):

                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Email or Password")

    with tab2:

        email = st.text_input("New Email")

        password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Create Account"):

            if register_user(email, password):

                st.success("Account Created")

            else:

                st.warning("Email already exists")

    st.stop()