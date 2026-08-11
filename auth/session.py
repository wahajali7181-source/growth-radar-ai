import streamlit as st


# ==========================================================
# LOGIN SESSION
# ==========================================================

def login_session(user):

    st.session_state["logged_in"] = True

    st.session_state["user"] = user


# ==========================================================
# LOGOUT
# ==========================================================

def logout_session():

    st.session_state.pop(
        "logged_in",
        None
    )

    st.session_state.pop(
        "user",
        None
    )


# ==========================================================
# CHECK LOGIN
# ==========================================================

def is_logged_in():

    return bool(
        st.session_state.get(
            "logged_in",
            False
        )
    )


# ==========================================================
# CURRENT USER
# ==========================================================

def current_user():

    return st.session_state.get(
        "user"
    )


# ==========================================================
# REQUIRE AUTH
# ==========================================================

def require_auth():

    if not is_logged_in():

        st.error(
            "🔒 Please login first."
        )

        st.stop()

    user = current_user()

    if not user:

        logout_session()

        st.error(
            "🔒 Session expired. Please login again."
        )

        st.stop()

    if user.get("status") == "Suspended":

        logout_session()

        st.error(
            "🚫 Your account has been suspended."
        )

        st.stop()


# ==========================================================
# REQUIRE ROLE
# ==========================================================

def require_role(role):

    user = current_user()

    if not user:

        st.error(
            "🔒 Please login first."
        )

        st.stop()

    if user.get("role") != role:

        st.error(
            "⛔ Access Denied"
        )

        st.stop()