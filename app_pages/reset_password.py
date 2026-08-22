import streamlit as st

from auth.password import (
    verify_reset_token,
    reset_password,
)


def show():

    st.title("🔐 Reset Password")

    st.caption(
        "Create a new password for your Growth Radar AI account."
    )

    st.divider()

    # ==========================================================
    # GET TOKEN FROM URL
    # ==========================================================

    token = st.query_params.get(
        "token",
        ""
    )

    if not token:

        st.error(
            "❌ Invalid or missing password reset link."
        )

        st.info(
            "Please request a new password reset link."
        )

        return

    # ==========================================================
    # VERIFY TOKEN
    # ==========================================================

    valid, token_data = verify_reset_token(
        token
    )

    if not valid:

        st.error(
            "❌ This password reset link is invalid "
            "or has expired."
        )

        st.info(
            "Please request a new password reset link."
        )

        return

    # ==========================================================
    # VALID TOKEN
    # ==========================================================

    st.success(
        "✅ Reset link verified."
    )

    st.subheader(
        "🔑 Create New Password"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        key="reset_new_password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        key="reset_confirm_password"
    )

    st.caption(
        "Password must be at least 8 characters and "
        "contain uppercase, lowercase, and a number."
    )

    st.divider()

    # ==========================================================
    # RESET PASSWORD
    # ==========================================================

    if st.button(
        "🔄 Reset Password",
        use_container_width=True,
        key="reset_password_button"
    ):

        success, message = reset_password(
            token,
            new_password,
            confirm_password
        )

        if success:

            st.success(
                "✅ Your password has been reset successfully."
            )

            st.info(
                "You can now return to the login page "
                "and sign in with your new password."
            )

            # Remove reset token from URL
            st.query_params.clear()

            # Clear password fields
            st.session_state.pop(
                "reset_new_password",
                None
            )

            st.session_state.pop(
                "reset_confirm_password",
                None
            )

        else:

            st.error(
                message
            )