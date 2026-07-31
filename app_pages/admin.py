import streamlit as st

from auth.session import require_role

from admin.stats import (
    total_users,
    premium_users,
    free_users
)

from admin.users import (
    get_all_users,
    make_admin,
    suspend_user,
    activate_user,
    delete_user
)


def show():

    require_role("Admin")

    st.title("👑 Admin Dashboard")

    st.caption("Growth Radar AI Control Center")

    st.divider()

    # ==========================
    # Stats
    # ==========================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👥 Total Users",
        total_users()
    )

    c2.metric(
        "💎 Premium",
        premium_users()
    )

    c3.metric(
        "🆓 Free",
        free_users()
    )

    st.divider()

    # ==========================
    # Users
    # ==========================

    st.subheader("👥 User Management")

    users = get_all_users()

    for user in users:

        name = user[0]
        email = user[1]
        role = user[2]
        plan = user[3]
        status = user[4]
        created = user[5]

        with st.expander(f"{name} ({email})"):

            st.write(f"**Role:** {role}")
            st.write(f"**Plan:** {plan}")
            st.write(f"**Status:** {status}")
            st.write(f"**Created:** {created}")

            c1, c2, c3, c4 = st.columns(4)

            if c1.button(
                "👑 Admin",
                key=f"admin_{email}"
            ):
                make_admin(email)
                st.success("User is now Admin")
                st.rerun()

            if status == "Active":

                if c2.button(
                    "🚫 Suspend",
                    key=f"suspend_{email}"
                ):
                    suspend_user(email)
                    st.success("User Suspended")
                    st.rerun()

            else:

                if c2.button(
                    "✅ Activate",
                    key=f"activate_{email}"
                ):
                    activate_user(email)
                    st.success("User Activated")
                    st.rerun()

            if c3.button(
                "🗑 Delete",
                key=f"delete_{email}"
            ):
                delete_user(email)
                st.success("User Deleted")
                st.rerun()

            c4.write(plan)

    st.divider()

    st.success("Admin Dashboard Connected Successfully")