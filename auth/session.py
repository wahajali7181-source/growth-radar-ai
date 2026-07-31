import streamlit as st


def login_session(user):

    st.session_state["logged_in"] = True
    st.session_state["user"] = user


def logout_session():

    st.session_state.clear()


def is_logged_in():

    return st.session_state.get("logged_in", False)


def current_user():

    return st.session_state.get("user", None)
def require_auth():

    if not is_logged_in():

        st.error("🔒 Please login first.")

        st.stop()


def require_role(role):

    user = current_user()

    if not user:

        st.stop()

    if user["role"] != role:

        st.error("⛔ Access Denied")

        st.stop()