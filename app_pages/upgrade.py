import streamlit as st

from auth.session import current_user
from subscriptions.engine import get_user_plan
from payments.gateway import PLANS


def show():

    user = current_user()

    if not user:
        st.error("Please login first.")
        return

    plan = get_user_plan(user["email"])

    st.title("💳 Upgrade Plan")

    st.caption("Choose the best plan for your business.")

    st.divider()

    st.success(f"Current Plan: {plan}")

    st.divider()

    cols = st.columns(3)

    plans = list(PLANS.items())

    for i, (plan_name, info) in enumerate(plans):

        with cols[i]:

            st.subheader(plan_name)

            st.markdown(f"### Rs. {info['price']:,}")

            st.caption(info["duration"])

            st.write("")

            if plan == plan_name.upper():

                st.success("Current Plan")

            else:

                if st.button(
                    f"Upgrade to {plan_name}",
                    key=f"upgrade_{plan_name}",
                    width="stretch"
                ):

                    st.info(
                        "Payment Gateway will be connected in the next phase."
                    )