import os
import streamlit as st

from auth.session import require_auth, current_user

from website_builder.database import (
    get_user_websites,
    get_website_by_id,
    delete_website_record,
)


# ==========================================================
# PAGE CONFIG / AUTH
# ==========================================================

require_auth()

user = current_user()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🌐 My Websites")

st.caption(
    "Manage the websites you have created with Growth Radar AI."
)


# ==========================================================
# CURRENT USER
# ==========================================================

user_id = user.get("id")

if not user_id:

    st.error(
        "Unable to identify your account."
    )

    st.stop()


# ==========================================================
# LOAD USER WEBSITES
# ==========================================================

websites = get_user_websites(
    user_id
)


# ==========================================================
# EMPTY STATE
# ==========================================================

if not websites:

    st.info(
        "You have not created any websites yet."
    )

    st.caption(
        "Go to AI Website Builder to create your first website."
    )

    st.stop()


# ==========================================================
# SUMMARY
# ==========================================================

total_websites = len(
    websites
)

live_websites = len(
    [
        website
        for website in websites
        if website.get("live_url")
    ]
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Websites",
        total_websites,
    )

with col2:

    st.metric(
        "Live Websites",
        live_websites,
    )


st.divider()


# ==========================================================
# WEBSITE LIST
# ==========================================================

for website in websites:

    website_id = website.get(
        "id"
    )

    business_name = website.get(
        "business_name",
        "Unnamed Website",
    )

    business_type = website.get(
        "business_type",
        ""
    )

    status = website.get(
        "status",
        "generated",
    )

    folder_path = website.get(
        "folder_path",
        ""
    )

    live_url = website.get(
        "live_url"
    )


    with st.container(
        border=True
    ):

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.subheader(
                business_name
            )

            if business_type:

                st.caption(
                    business_type
                )

            st.write(
                f"Status: **{status.title()}**"
            )

            if live_url:

                st.success(
                    f"Live: {live_url}"
                )

        with col2:

            st.caption(
                "Website Actions"
            )

            if st.button(
                "Manage",
                key=f"manage_{website_id}",
                use_container_width=True,
            ):

                selected_website = get_website_by_id(
                    website_id,
                    user_id,
                )

                if selected_website:

                    st.session_state[
                        "current_website_id"
                    ] = selected_website.get(
                        "id"
                    )

                    st.session_state[
                        "current_website_folder"
                    ] = selected_website.get(
                        "folder_path"
                    )

                    st.session_state[
                        "current_website_record"
                    ] = selected_website

                    st.success(
                        "Website selected successfully."
                    )

                else:

                    st.error(
                        "Unable to load this website."
                    )


            if st.button(
                "Delete",
                key=f"delete_{website_id}",
                use_container_width=True,
            ):

                delete_result = delete_website_record(
                    website_id,
                    user_id,
                )

                if delete_result.get(
                    "success"
                ):

                    if (
                        st.session_state.get(
                            "current_website_id"
                        )
                        == website_id
                    ):

                        st.session_state.pop(
                            "current_website_id",
                            None
                        )

                        st.session_state.pop(
                            "current_website_folder",
                            None
                        )

                        st.session_state.pop(
                            "current_website_record",
                            None
                        )

                    st.success(
                        "Website removed from your account."
                    )

                    st.rerun()

                else:

                    st.error(
                        delete_result.get(
                            "message",
                            "Unable to delete website.",
                        )
                    )


        if folder_path:

            st.caption(
                f"Created: {website.get('created_at', '')}"
            )

            if not os.path.isdir(
                folder_path
            ):

                st.warning(
                    "Website files are not available on this server."
                )