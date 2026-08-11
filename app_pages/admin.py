import streamlit as st

from auth.session import (
    require_role,
    current_user
)

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

from payments.database import (
    create_payments_table,
    get_all_payments_requests,
    approve_payments,
    reject_payments
)

from subscriptions.database import (
    update_plan
)


def show():

    # ==========================================================
    # ADMIN AUTH
    # ==========================================================

    require_role(
        "Admin"
    )

    user = current_user()

    admin_email = user.get(
        "email",
        "Admin"
    )

    create_payments_table()

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title(
        "👑 Admin Dashboard"
    )

    st.caption(
        "Growth Radar AI Control Center"
    )

    st.divider()

    # ==========================================================
    # STATS
    # ==========================================================

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

    # ==========================================================
    # PAYMENT APPROVALS
    # ==========================================================

    st.subheader(
        "💳 Payment Approvals"
    )

    payment_requests = (
        get_all_payments_requests()
    )

    pending_requests = [

        request

        for request in payment_requests

        if request[6] == "Pending"

    ]

    if not pending_requests:

        st.success(
            "No pending payment requests."
        )

    else:

        st.info(
            f"{len(pending_requests)} "
            f"payment request(s) waiting for approval."
        )

        for request in pending_requests:

            (
                request_id,
                email,
                plan,
                amount,
                method,
                transaction_id,
                status,
                created_at,
                reviewed_at,
                reviewed_by

            ) = request

            with st.expander(

                f"#{request_id} — "
                f"{email} — "
                f"{plan} — "
                f"Rs. {amount:,}"

            ):

                st.write(
                    f"**User:** {email}"
                )

                st.write(
                    f"**Requested Plan:** {plan}"
                )

                st.write(
                    f"**Amount:** Rs. {amount:,}"
                )

                st.write(
                    f"**Payment Method:** {method}"
                )

                st.write(
                    f"**Transaction ID:** "
                    f"{transaction_id}"
                )

                st.write(
                    f"**Submitted:** {created_at}"
                )

                st.warning(
                    "Verify the payment transaction before approving "
                    "the subscription upgrade."
                    
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(

                        "✅ Approve Payment",

                        key=f"approve_{request_id}",

                        use_container_width=True

                    ):

                        # First update subscription
                        update_plan(
                            email,
                            plan
                        )

                        approved = approve_payments(

                            request_id,

                            admin_email

                        )

                        if approved:

                            st.success(
                                f"{email} upgraded to "
                                f"{plan} successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to approve payment."
                            )

                with col2:

                    if st.button(

                        "❌ Reject Payment",

                        key=f"reject_{request_id}",

                        use_container_width=True

                    ):

                        rejected = reject_payments(

                            request_id,

                            admin_email

                        )

                        if rejected:

                            st.success(
                                "Payment request rejected."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to reject payment."
                            )

    # ==========================================================
    # PAYMENT HISTORY
    # ==========================================================

    st.divider()

    st.subheader(
        "📜 Payment History"
    )

    if payment_requests:

        import pandas as pd

        payment_rows = []

        for request in payment_requests:

            payment_rows.append({

                "ID": request[0],

                "Email": request[1],

                "Plan": request[2],

                "Amount": request[3],

                "Method": request[4],

                "Transaction ID": request[5],

                "Status": request[6],

                "Created": request[7],

                "Reviewed": request[8],

            })

        payment_df = pd.DataFrame(
            payment_rows
        )

        st.dataframe(

            payment_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.caption(
            "No payment history available."
        )

    st.divider()

    # ==========================================================
    # USERS
    # ==========================================================

    st.subheader(
        "👥 User Management"
    )

    users = get_all_users()

    for user in users:

        name = user[0]

        email = user[1]

        role = user[2]

        plan = user[3]

        status = user[4]

        created = user[5]

        with st.expander(

            f"{name} ({email})"

        ):

            st.write(
                f"**Role:** {role}"
            )

            st.write(
                f"**Plan:** {plan}"
            )

            st.write(
                f"**Status:** {status}"
            )

            st.write(
                f"**Created:** {created}"
            )

            c1, c2, c3, c4 = st.columns(4)

            if c1.button(

                "👑 Admin",

                key=f"admin_{email}"

            ):

                make_admin(email)

                st.success(
                    "User is now Admin."
                )

                st.rerun()

            if status == "Active":

                if c2.button(

                    "🚫 Suspend",

                    key=f"suspend_{email}"

                ):

                    suspend_user(email)

                    st.success(
                        "User suspended."
                    )

                    st.rerun()

            else:

                if c2.button(

                    "✅ Activate",

                    key=f"activate_{email}"

                ):

                    activate_user(email)

                    st.success(
                        "User activated."
                    )

                    st.rerun()

            if c3.button(

                "🗑 Delete",

                key=f"delete_{email}"

            ):

                delete_user(email)

                st.success(
                    "User deleted."
                )

                st.rerun()

            c4.write(
                plan
            )

    st.divider()

    st.success(
        "Admin Dashboard Connected Successfully"
    )