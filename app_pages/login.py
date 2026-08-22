import streamlit as st

from auth.login import login_user
from auth.session import login_session

from auth.password import (
    create_reset_token,
)

# ==========================================================
# LOGIN PAGE
# ==========================================================

def show():

    st.title("🔐 Login")

    st.caption(
        "Login to Growth Radar AI"
    )

    st.divider()

    # ======================================================
    # FORGOT PASSWORD MODE
    # ======================================================

    if st.session_state.get(
        "forgot_password",
        False
    ):

        st.subheader(
            "🔑 Forgot Password"
        )

        st.caption(
            "Enter your registered email address and "
            "we'll send you a password reset link."
        )

        reset_email = st.text_input(
            "Email",
            key="reset_email"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📩 Send Reset Link",
                key="generate_reset",
                use_container_width=True
            ):

                if not reset_email.strip():

                    st.error(
                        "Please enter your email address."
                    )

                else:

                    success, result = create_reset_token(
                        reset_email
                    )

                    # Do not reveal whether email exists.
                    st.success(
                        "If this email is registered, "
                        "a password reset link has been "
                        "sent to your email."
                    )

        with col2:

            if st.button(
                "← Back to Login",
                key="back_to_login",
                use_container_width=True
            ):

                st.session_state[
                    "forgot_password"
                ] = False

                st.session_state.pop(
                    "reset_email",
                    None
                )

                st.rerun()

        return

    # ======================================================
    # NORMAL LOGIN
    # ======================================================

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    # ======================================================
    # FORGOT PASSWORD
    # ======================================================

    if st.button(
        "🔑 Forgot Password?",
        key="forgot_password_button",
        use_container_width=True
    ):

        st.session_state[
            "forgot_password"
        ] = True

        st.rerun()

    st.divider()

    # ======================================================
    # LOGIN
    # ======================================================

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

            login_session(
                result
            )

            st.success(
                f"Welcome back, {result['name']}!"
            )

            st.rerun()

        else:

            st.error(
                result
            )