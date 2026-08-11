import streamlit as st

from auth.session import current_user
from subscriptions.engine import get_user_plan
from subscriptions.plans import get_all_plans
from payments.gateway import (
    get_checkout_url,
    get_bank_transfer_details,
)
from payments.database import (
    create_payment,
    get_user_payments,
)


def show():

    # ==========================================================
    # AUTH
    # ==========================================================

    user = current_user()

    if not user:

        st.error(
            "🔒 Please login first."
        )

        return

    user_email = user["email"]

    # ==========================================================
    # USER PLAN
    # ==========================================================

    current_plan = get_user_plan(
        user_email
    )

    current_plan = current_plan.upper()

    plans = get_all_plans()

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title(
        "💳 Upgrade Growth Radar AI"
    )

    st.caption(
        "Choose the plan that fits your business growth."
    )

    st.divider()

    # ==========================================================
    # CURRENT PLAN
    # ==========================================================

    current_plan_info = plans.get(
        current_plan,
        plans["FREE"]
    )

    st.success(
        f"Current Plan: {current_plan_info['name']} ✓"
    )

    st.divider()

    # ==========================================================
    # PLAN ORDER
    # ==========================================================

    plan_order = [

        "FREE",
        "STARTER",
        "PROFESSIONAL",
        "AGENCY"

    ]

    available_plans = [

        plan
        for plan in plan_order
        if plan in plans

    ]

    # ==========================================================
    # PLAN CARDS
    # ==========================================================

    cols = st.columns(
        len(available_plans)
    )

    for index, plan_name in enumerate(
        available_plans
    ):

        plan = plans[plan_name]

        with cols[index]:

            # --------------------------------------------------
            # BADGE
            # --------------------------------------------------

            if plan_name == current_plan:

                st.success(
                    "✓ CURRENT PLAN"
                )

            elif plan_name == "PROFESSIONAL":

                st.info(
                    "⭐ MOST POPULAR"
                )

            elif plan_name == "AGENCY":

                st.warning(
                    "🏢 FOR AGENCIES"
                )

            else:

                st.write("")

            # --------------------------------------------------
            # PLAN NAME
            # --------------------------------------------------

            st.subheader(
                plan["name"]
            )

            # --------------------------------------------------
            # PRICE
            # --------------------------------------------------

            price = plan.get(
                "price",
                0
            )

            if price == 0:

                st.markdown(
                    "## Free"
                )

            else:

                st.markdown(
                    f"## ${price}"
                )

                st.caption(
                    "per month"
                )

            st.divider()

            # --------------------------------------------------
            # FEATURES
            # --------------------------------------------------

            features = plan.get(
                "features",
                {}
            )

            st.markdown(
                "**Included:**"
            )

            for feature, limit in features.items():

                if isinstance(
                    limit,
                    bool
                ):

                    if limit:

                        st.write(
                            f"✅ {feature.replace('_', ' ').title()}"
                        )

                    continue

                if limit == -1:

                    st.write(
                        f"♾️ {feature.replace('_', ' ').title()} — Unlimited"
                    )

                else:

                    st.write(
                        f"✅ {feature.replace('_', ' ').title()} — {limit}"
                    )

            st.write("")

            # --------------------------------------------------
            # BUTTON
            # --------------------------------------------------

            if plan_name == current_plan:

                st.button(
                    "✓ Current Plan",
                    key=f"current_{plan_name}",
                    use_container_width=True,
                    disabled=True
                )

            elif plan_name == "FREE":

                st.button(
                    "Free Plan",
                    key=f"free_{plan_name}",
                    use_container_width=True,
                    disabled=True
                )

            else:

                checkout_url = get_checkout_url(
                    plan_name
                )

                if checkout_url:

                    st.link_button(
                        f"🚀 Upgrade to {plan['name']}",
                        checkout_url,
                        use_container_width=True
                    )

                else:

                    st.button(
                        f"🚀 Upgrade to {plan['name']}",
                        key=f"upgrade_{plan_name}",
                        use_container_width=True,
                        disabled=True
                    )

                    st.caption(
                        "Online checkout will be available soon."
                    )

    # ==========================================================
    # PAYMENT METHODS
    # ==========================================================

    st.divider()

    st.subheader(
        "💰 Payment Methods"
    )

    st.caption(
        "Choose online checkout or submit a bank transfer for manual verification."
    )

    payment_col1, payment_col2 = st.columns(2)

    # ==========================================================
    # LEMON SQUEEZY
    # ==========================================================

    with payment_col1:

        st.markdown(
            "### 💳 Lemon Squeezy"
        )

        st.write(
            "Pay securely online using supported "
            "card and digital payment methods."
        )

        st.success(
            "Secure Online Checkout"
        )

        st.caption(
            "Online checkout will become active when "
            "the plan checkout URLs are configured."
        )

    # ==========================================================
    # BANK TRANSFER
    # ==========================================================

    with payment_col2:

        st.markdown(
            "### 🏦 Bank Transfer"
        )

        st.write(
            "Transfer the subscription amount and "
            "submit your transaction ID for verification."
        )

        bank = get_bank_transfer_details()

        with st.expander(
            "🏦 View Bank Transfer Details"
        ):

            account_title = bank.get(
                "account_title",
                ""
            )

            bank_name = bank.get(
                "bank_name",
                ""
            )

            account_number = bank.get(
                "account_number",
                ""
            )

            iban = bank.get(
                "iban",
                ""
            )

            if account_title:

                st.write(
                    f"**Account Title:** {account_title}"
                )

            if bank_name:

                st.write(
                    f"**Bank:** {bank_name}"
                )

            if account_number:

                st.write(
                    f"**Account Number:** {account_number}"
                )

            if iban:

                st.write(
                    f"**IBAN:** {iban}"
                )

            if not (
                account_number
                or iban
            ):

                st.warning(
                    "Bank details have not been configured yet."
                )

            st.info(
                bank.get(
                    "instructions",
                    "Complete the bank transfer and submit your transaction ID."
                )
            )

    # ==========================================================
    # MANUAL PAYMENT FORM
    # ==========================================================

    st.divider()

    st.subheader(
        "🧾 Submit Bank Transfer"
    )

    st.caption(
        "After making the transfer, submit the details below. "
        "Your payment will remain PENDING until an administrator verifies it."
    )

    paid_plan = st.selectbox(
        "Select the plan you paid for",
        [
            "STARTER",
            "PROFESSIONAL",
            "AGENCY"
        ],
        format_func=lambda plan: (
            f"{plans[plan]['name']} — "
            f"${plans[plan]['price']}/month"
        ),
        key="bank_payment_plan"
    )

    paid_plan_info = plans[
        paid_plan
    ]

    st.info(
        f"You are submitting payment for "
        f"**{paid_plan_info['name']}** — "
        f"**${paid_plan_info['price']} / month**"
    )

    transaction_id = st.text_input(
        "Transaction / Reference ID",
        placeholder="Enter your bank transaction ID",
        key="bank_transaction_id"
    )

    payment_note = st.text_area(
        "Payment Note (Optional)",
        placeholder="Any additional payment information...",
        key="bank_payment_note"
    )

    if st.button(
        "📤 Submit Payment for Verification",
        use_container_width=True,
        type="primary"
    ):

        transaction_id = transaction_id.strip()

        if not transaction_id:

            st.warning(
                "Please enter your transaction/reference ID."
            )

        else:

            amount = paid_plan_info.get(
                "price",
                0
            )

            try:

                payment_id = create_payment(
                    user_email=user_email,
                    plan=paid_plan,
                    amount=amount,
                    payment_method="Bank Transfer",
                    transaction_id=transaction_id
                )

                st.success(
                    "✅ Payment submitted successfully!"
                )

                st.info(
                    f"Payment ID: **#{payment_id}**"
                )

                st.caption(
                    "Status: PENDING — An administrator must verify "
                    "your payment before the plan is activated."
                )

            except Exception as e:

                st.error(
                    "Unable to submit payment."
                )

                st.caption(
                    str(e)
                )

    # ==========================================================
    # USER PAYMENT HISTORY
    # ==========================================================

    st.divider()

    st.subheader(
        "📋 Your Payment History"
    )

    try:

        payments = get_user_payments(
            user_email
        )

        if not payments:

            st.info(
                "You have no payment requests yet."
            )

        else:

            for payment in payments:

                payment_id = payment[0]
                plan = payment[2]
                amount = payment[3]
                method = payment[4]
                transaction = payment[5]
                status = payment[6]
                created_at = payment[7]
                verified_at = payment[8]

                with st.container():

                    st.markdown(
                        f"### Payment #{payment_id}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.write(
                            f"**Plan:** {plan}"
                        )

                        st.write(
                            f"**Amount:** ${amount}"
                        )

                    with col2:

                        st.write(
                            f"**Method:** {method}"
                        )

                        st.write(
                            f"**Transaction:** {transaction}"
                        )

                    with col3:

                        if status == "VERIFIED":

                            st.success(
                                "✅ VERIFIED"
                            )

                        elif status == "PENDING":

                            st.warning(
                                "⏳ PENDING"
                            )

                        else:

                            st.error(
                                f"❌ {status}"
                            )

                        st.caption(
                            f"Created: {created_at}"
                        )

                        if verified_at:

                            st.caption(
                                f"Verified: {verified_at}"
                            )

                    st.divider()

    except Exception as e:

        st.warning(
            "Payment history is temporarily unavailable."
        )

        st.caption(
            str(e)
        )

    # ==========================================================
    # BILLING INFORMATION
    # ==========================================================

    st.info(
        """
💡 **How billing works**

• Your subscription is billed monthly.

• Your plan determines your feature limits.

• AI-heavy features have controlled usage limits.

• When a limit is reached, you can upgrade to a higher plan.

• Bank-transfer payments require manual verification.

• Your plan is activated only after payment verification.
"""
    )