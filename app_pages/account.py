import streamlit as st

from auth.session import (
    require_auth,
    current_user,
    logout_session
)


def show():

    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    require_auth()

    user = current_user()

    if not user:

        st.error(
            "No user session found."
        )

        return

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title(
        "👤 My Account"
    )

    st.caption(
        "Manage your Growth Radar AI account."
    )

    st.divider()

    # ==========================================================
    # ACCOUNT OVERVIEW
    # ==========================================================

    st.subheader(
        "📊 Account Overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Plan",
            user.get(
                "plan",
                "Free"
            )
        )

    with col2:

        st.metric(
            "Account Role",
            user.get(
                "role",
                "User"
            )
        )

    with col3:

        st.metric(
            "Status",
            user.get(
                "subscription_status",
                "Active"
            )
        )

    st.divider()

    # ==========================================================
    # PROFILE
    # ==========================================================

    st.subheader(
        "👤 Profile"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(

            "Full Name",

            value=str(
                user.get(
                    "name",
                    user.get(
                        "full_name",
                        ""
                    )
                )
            ),

            disabled=True

        )

    with col2:

        st.text_input(

            "Email",

            value=str(
                user.get(
                    "email",
                    ""
                )
            ),

            disabled=True

        )

    st.divider()

    # ==========================================================
    # SUBSCRIPTION
    # ==========================================================

    st.subheader(
        "💳 Subscription"
    )

    plan = user.get(
        "plan",
        "Free"
    )

    subscription_status = user.get(
        "subscription_status",
        "Active"
    )

    trial_expiry = user.get(
        "trial_expiry",
        ""
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
**Current Plan**

{plan}

**Status**

{subscription_status}
"""
        )

    with col2:

        if trial_expiry:

            st.info(
                f"""
**Trial Expiry**

{trial_expiry}
"""
            )

        else:

            st.info(
                """
**Trial Expiry**

Not available
"""
            )

    st.divider()

    # ==========================================================
    # USAGE
    # ==========================================================

    st.subheader(
        "📈 Usage"
    )

    usage_count = user.get(
        "usage_count",
        0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Platform Usage",
            usage_count
        )

    with col2:

        st.metric(
            "Website Audits",
            "—"
        )

    with col3:

        st.metric(
            "Leads",
            "—"
        )

    st.caption(
        "Detailed usage analytics will be connected to the platform modules as their usage tracking is finalized."
    )

    st.divider()

    # ==========================================================
    # SECURITY
    # ==========================================================

    st.subheader(
        "🔐 Security"
    )

    st.info(
        "Password change and advanced security settings will be available in a future update."
    )

    st.divider()

    # ==========================================================
    # LOGOUT
    # ==========================================================

    st.subheader(
        "🚪 Session"
    )

    st.caption(
        "Logging out will end your current Growth Radar AI session."
    )

    if st.button(

        "🚪 Logout",

        use_container_width=True

    ):

        logout_session()

        st.success(
            "Logged out successfully."
        )

        st.rerun()