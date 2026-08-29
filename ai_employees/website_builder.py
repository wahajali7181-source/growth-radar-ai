import os
import streamlit as st


from website_builder.engine import generate_complete_website

from website_builder.publisher import (
    start_preview_server,
    stop_preview_server,
    publish_website,
)

from website_builder.editor import (
    edit_website,
    get_edit_summary,
)

from website_builder.ai_editor import (
    execute_ai_edit,
)

from website_builder.preview import show_preview

from auth.session import current_user
from website_builder.database import (
    create_website_record,
    get_user_websites,
    get_website_by_id,
    update_website_record,
    delete_website_record,
)

# ==========================================================
# HELPERS
# ==========================================================

def _stop_existing_preview():

    preview_state = st.session_state.get(
        "website_live_preview"
    )

    if not preview_state:

        return

    process_id = preview_state.get(
        "pid"
    )

    if process_id:

        try:

            stop_preview_server(
                process_id
            )

        except Exception:
            pass

    st.session_state.pop(
        "website_live_preview",
        None
    )


def _reset_publish_state():

    st.session_state.pop(
        "website_publish_result",
        None
    )


def _mark_website_changed():

    # The current local preview belongs to the old version.
    _stop_existing_preview()

    # Existing publish result must be cleared because
    # the website now contains unpublished changes.
    _reset_publish_state()

    st.session_state[
        "website_has_unsaved_changes"
    ] = True

    # --------------------------------------------------
    # UPDATE WEBSITE ACTIVITY
    # --------------------------------------------------

    current_website_id = st.session_state.get(
        "current_website_id"
    )

    user = current_user()

    if (
        current_website_id
        and user
        and user.get("id")
    ):

        update_result = update_website_record(
            current_website_id,
            user.get("id"),
            status="generated",
        )

        if not update_result.get("success"):

            print(
                "[Website Builder] "
                "Unable to update website activity:",
                update_result
            )


# ==========================================================
# AI WEBSITE BUILDER
# ==========================================================

def show():

    st.title(
        "🌐 AI Website Builder"
    )

    st.caption(
        "Generate, preview, edit, build and publish a professional business website."
    )

    st.divider()

    # ======================================================
    # BUSINESS INFORMATION
    # ======================================================

    st.subheader(
        "🏢 Business Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        business_name = st.text_input(
            "Business Name",
            placeholder="Example: Bright Dental Clinic",
            key="website_business_name",
        )

        business_type = st.text_input(
            "Business Type",
            placeholder="Example: Dentist, Gym, Real Estate",
            key="website_business_type",
        )

    with col2:

        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Local patients",
            key="website_target_audience",
        )

        cta = st.text_input(
            "Primary CTA",
            placeholder="Example: Book Appointment",
            key="website_cta",
        )

    st.divider()

    # ======================================================
    # WEBSITE DESIGN
    # ======================================================

    st.subheader(
        "🎨 Website Design"
    )

    col1, col2 = st.columns(2)

    with col1:

        style = st.selectbox(
            "Website Style",
            [
                "Modern Professional",
                "Premium",
                "Minimal",
                "Corporate",
                "Luxury",
                "Creative",
                "Clean & Friendly",
            ],
            key="website_style",
        )

    with col2:

        colors = st.text_input(
            "Primary Colors",
            placeholder="#2563EB, #FFFFFF",
            key="website_colors",
        )

    pages = st.multiselect(
        "Website Pages / Sections",
        [
            "Home",
            "About",
            "Services",
            "Testimonials",
            "FAQ",
            "Contact",
        ],
        default=[
            "Home",
            "About",
            "Services",
            "FAQ",
            "Contact",
        ],
        key="website_pages",
    )

    st.divider()

    # ======================================================
    # GENERATE WEBSITE
    # ======================================================

    if st.button(
        "🚀 Generate Complete Website",
        use_container_width=True,
        key="website_generate",
    ):

        if not business_name.strip():

            st.warning(
                "Please enter the Business Name."
            )

            return

        if not business_type.strip():

            st.warning(
                "Please enter the Business Type."
            )

            return

        if not target_audience.strip():

            st.warning(
                "Please enter the Target Audience."
            )

            return

        if not cta.strip():

            st.warning(
                "Please enter the Primary CTA."
            )

            return

        if not pages:

            st.warning(
                "Please select at least one page."
            )

            return

        # --------------------------------------------------
        # STOP OLD PREVIEW
        # --------------------------------------------------

        _stop_existing_preview()

        # --------------------------------------------------
        # GENERATE
        # --------------------------------------------------

        with st.spinner(
            "🤖 AI Website Builder is creating your website..."
        ):

            result = generate_complete_website(

                business_name=business_name.strip(),

                business_type=business_type.strip(),

                audience=target_audience.strip(),

                style=style,

                colors=colors.strip(),

                pages=", ".join(
                    pages
                ),

                cta=cta.strip(),
            )

        # --------------------------------------------------
        # FAILURE
        # --------------------------------------------------

        if not result:

            st.error(
                "Website generation failed."
            )

            return

        if not result.get(
            "success"
        ):

            st.error(
                result.get(
                    "error",
                    "Website generation failed.",
                )
            )

            reason = result.get(
                "reason"
            )

            if reason:

                st.caption(
                    f"Reason: {reason}"
                )

            guardrail = result.get(
                "guardrail"
            )

            if guardrail:

                st.warning(
                    guardrail.get(
                        "reason",
                        "Website guardrail rejected the output.",
                    )
                )

            return

        # SAVE WEBSITE TO CURRENT USER ACCOUNT
        # --------------------------------------------------

        user = current_user()

        if not user or not user.get("id"):

            st.error(
                "Unable to identify the current user."
            )

            return

        user_id = user.get(
            "id"
        )

        generated_folder = result.get(
            "folder"
        )

        website_record = create_website_record(
            user_id=user_id,
            business_name=business_name.strip(),
            business_type=business_type.strip(),
            folder_path=generated_folder,
        )

        if not website_record.get(
            "success"
        ):

            st.error(
                website_record.get(
                    "message",
                    "Unable to save website to your account.",
                )
            )

            return

        result[
            "website_id"
        ] = website_record.get(
            "website_id"
        )

        st.session_state[
            "current_website_id"
        ] = website_record.get(
            "website_id"
        )

        # --------------------------------------------------
        # SAVE RESULT
        # --------------------------------------------------

        st.session_state[
            "website_builder_result"
        ] = result

        st.session_state[
            "website_has_unsaved_changes"
        ] = False

        st.session_state.pop(
            "website_publish_result",
            None
        )

        st.session_state.pop(
            "website_edit_result",
            None
        )

        st.success(
            "Website generated successfully!"
        )

    
        st.rerun()
    # ======================================================
    # MY WEBSITES
    # ======================================================

    user = current_user()

    if user and user.get("id"):

        user_id = user.get("id")

        saved_websites = get_user_websites(
            user_id
        )

        if saved_websites:
                    # --------------------------------------------------
            # WEBSITE DASHBOARD SUMMARY
            # --------------------------------------------------

            total_websites = len(
                saved_websites
            )

            published_websites = sum(
                1
                for website in saved_websites
                if str(
                    website.get(
                        "status",
                        ""
                    )
                ).lower() == "published"
            )

            generated_websites = sum(
                1
                for website in saved_websites
                if str(
                    website.get(
                        "status",
                        ""
                    )
                ).lower() == "generated"
            )
            live_websites = sum(
                1
                for website in saved_websites
                if website.get(
                    "live_url"
                )
            )

            summary_col1, summary_col2, summary_col3, summary_col4 = (
                st.columns(
                    4
                )
            )

            with summary_col1:

                st.metric(
                    "Total Websites",
                    total_websites,
                )

            with summary_col2:

                st.metric(
                    "Published",
                    published_websites,
                )

            with summary_col3:

                st.metric(
                    "Generated",
                    generated_websites,
                )    
            with summary_col4:

                st.metric(
                    "Live Websites",
                    live_websites,
                )
            st.divider()

            st.subheader(
                "🌐 My Websites"
            )

            st.caption(
                "Manage the websites saved to your account."
            )
            filter_col1, filter_col2, filter_col3 = st.columns(
                [2, 1, 1]
            )

            with filter_col1:

                website_search = st.text_input(
                    "Search websites",
                    placeholder="Search by business name or type...",
                    key="website_search",
                )

            with filter_col2:

                website_status_filter = st.selectbox(
                    "Status",
                    options=[
                        "All",
                        "Published",
                        "Generated",
                        "Live",
                    ],
                    key="website_status_filter",
                )
            with filter_col3:

                website_sort = st.selectbox(
                    "Sort By",
                    options=[
                        "Recently Updated",
                        "Newest Created",
                        "Oldest Created",
                        "Business Name A-Z",
                    ],
                    key="website_sort",
                )
            filtered_websites = []

            search_query = website_search.strip().lower()

            for website in saved_websites:

                website_name = str(
                    website.get(
                        "business_name",
                        ""
                    )
                ).lower()

                website_type = str(
                    website.get(
                        "business_type",
                        ""
                    )
                ).lower()

                website_status = str(
                    website.get(
                        "status",
                        ""
                    )
                ).lower()

                matches_search = (
                    not search_query
                    or search_query in website_name
                    or search_query in website_type
                )

                matches_status = (
                    website_status_filter == "All"
                    or (
                        website_status_filter == "Live"
                        and bool(
                            website.get(
                            "live_url"
                        )
                    )
                )
                    or (
                        website_status_filter != "Live"
                        and website_status
                        == website_status_filter.lower()
                    )
                )

                if (
                    matches_search
                    and matches_status
                ):

                    filtered_websites.append(
                        website
                    )
            if website_sort == "Recently Updated":

                filtered_websites.sort(
                    key=lambda website: (
                        website.get(
                            "updated_at"
                        )
                        or ""
                    ),
                    reverse=True,
                )

            elif website_sort == "Newest Created":

                filtered_websites.sort(
                    key=lambda website: (
                        website.get(
                            "created_at"
                        )
                        or ""
                    ),
                    reverse=True,
                )

            elif website_sort == "Oldest Created":

                filtered_websites.sort(
                    key=lambda website: (
                        website.get(
                            "created_at"
                        )
                        or ""
                    )
                )

            elif website_sort == "Business Name A-Z":

                filtered_websites.sort(
                    key=lambda website: str(
                        website.get(
                            "business_name",
                            ""
                        )
                    ).lower()
                )        
            if not filtered_websites:

                st.info(
                    "No websites match your search or filter."
                )

            for website in filtered_websites:        
            

                website_id = website.get(
                    "id"
                )

                business_name = website.get(
                    "business_name",
                    "Untitled Website",
                )

                business_type = website.get(
                    "business_type",
                    ""
                )

                status = website.get(
                    "status",
                    "generated",
                )
                status_key = str(
                    status or ""
                ).strip().lower()

                if status_key == "published":

                    status_label = "Published"

                elif status_key == "generated":

                    status_label = "Draft"

                else:

                    status_label = (
                        status.title()
                        if status
                        else "Unknown"
                    )

                created_at = website.get(
                    "created_at",
                    ""
                )

                updated_at = website.get(
                    "updated_at",
                    ""
                )

                live_url = website.get(
                    "live_url"
                )

                folder_path = website.get(
                    "folder_path"
                )

                with st.container(
                    border=True
                ):

                    header_col, status_col = st.columns(
                        [3, 1]
                    )

                    with header_col:

                        st.markdown(
                            f"### {business_name}"
                        )

                        if business_type:

                            st.caption(
                                f"Business Type: {business_type}"
                            )

                    with status_col:

                        if status_key == "published":

                            st.success(
                                "LIVE"
                            )

                        elif status_key == "generated":

                            st.info(
                                "DRAFT"
                            )

                        else:

                            st.warning(
                                status_label.upper()
                            )

                    info_col1, info_col2 = st.columns(
                        2
                    )

                    with info_col1:

                        if created_at:

                            st.caption(
                                f"Created: {created_at}"
                            )

                    with info_col2:

                        if updated_at:

                            st.caption(
                                f"Last Updated: {updated_at}"
                            )
                    action_col1, action_col2, action_col3 = st.columns(
                        3
                    )

                    # ------------------------------------------
                    # MANAGE
                    # ------------------------------------------

                    with action_col1:

                        if st.button(
                            "Manage",
                            key=f"manage_{website_id}",
                            use_container_width=True,
                        ):

                            if not folder_path:

                                st.error(
                                    "Website folder path is missing."
                                )

                            elif not os.path.isdir(
                                folder_path
                            ):

                                st.error(
                                    "Website files are no longer available."
                                )

                            else:

                                _stop_existing_preview()

                                st.session_state[
                                    "website_builder_result"
                                ] = {
                                    "success": True,
                                    "folder": folder_path,
                                    "website_id": website_id,
                                    "business_name": business_name,
                                    "business_type": business_type,
                                }

                                st.session_state[
                                    "current_website_id"
                                ] = website_id

                                st.session_state[
                                    "current_website_folder"
                                ] = folder_path

                                st.session_state[
                                    "website_has_unsaved_changes"
                                ] = False

                                st.session_state.pop(
                                    "website_publish_result",
                                    None,
                                )

                                st.session_state.pop(
                                    "website_edit_result",
                                    None,
                                )

                                st.success(
                                    "Website loaded successfully."
                                )

                                st.rerun()

                    # ------------------------------------------
                    # OPEN LIVE WEBSITE
                    # ------------------------------------------

                    with action_col2:

                        if live_url:

                            st.link_button(
                                "Open Live",
                                live_url,
                                use_container_width=True,
                            )

                        else:

                            st.button(
                                "Not Live",
                                disabled=True,
                                key=f"not_live_{website_id}",
                                use_container_width=True,
                            )

                                       # ------------------------------------------
                    # DELETE
                    # ------------------------------------------

                    with action_col3:

                        confirm_key = (
                            f"confirm_delete_{website_id}"
                        )

                        if not st.session_state.get(
                            confirm_key,
                            False,
                        ):

                            if st.button(
                                "Delete",
                                key=f"delete_{website_id}",
                                use_container_width=True,
                            ):

                                st.session_state[
                                    confirm_key
                                ] = True

                                st.rerun()

                        else:

                            st.warning(
                                "Delete this website?"
                            )

                            confirm_col, cancel_col = st.columns(
                                2
                            )

                            with confirm_col:

                                if st.button(
                                    "Yes, Delete",
                                    key=f"confirm_yes_{website_id}",
                                    use_container_width=True,
                                ):

                                    delete_result = (
                                        delete_website_record(
                                            website_id,
                                            user_id,
                                        )
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

                                            _stop_existing_preview()

                                            st.session_state.pop(
                                                "current_website_id",
                                                None,
                                            )

                                            st.session_state.pop(
                                                "current_website_folder",
                                                None,
                                            )

                                            st.session_state.pop(
                                                "website_builder_result",
                                                None,
                                            )

                                        st.session_state.pop(
                                            confirm_key,
                                            None,
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

                            with cancel_col:

                                if st.button(
                                    "Cancel",
                                    key=f"cancel_delete_{website_id}",
                                    use_container_width=True,
                                ):

                                    st.session_state.pop(
                                        confirm_key,
                                        None,
                                    )

                                    st.rerun()
                                        # ------------------------------------------
                    # EDIT WEBSITE DETAILS
                    # ------------------------------------------

                    with st.expander(
                        "Edit Website Details",
                        expanded=False,
                    ):

                        edited_business_name = st.text_input(
                            "Business Name",
                            value=business_name,
                            key=f"edit_name_{website_id}",
                        )

                        edited_business_type = st.text_input(
                            "Business Type",
                            value=business_type,
                            key=f"edit_type_{website_id}",
                        )

                        if st.button(
                            "Save Details",
                            key=f"save_details_{website_id}",
                            use_container_width=True,
                        ):

                            edited_business_name = (
                                edited_business_name.strip()
                            )

                            edited_business_type = (
                                edited_business_type.strip()
                            )

                            if not edited_business_name:

                                st.error(
                                    "Business name is required."
                                )

                            else:

                                update_result = (
                                    update_website_record(
                                        website_id,
                                        user_id=user_id,
                                        business_name=
                                            edited_business_name,
                                        business_type=
                                            edited_business_type,
                                    )
                                )

                                if update_result.get(
                                    "success"
                                ):

                                    # Update currently loaded
                                    # website session if necessary.
                                    if (
                                        st.session_state.get(
                                            "current_website_id"
                                        )
                                        == website_id
                                    ):

                                        current_result = (
                                            st.session_state.get(
                                                "website_builder_result"
                                            )
                                        )

                                        if current_result:

                                            current_result[
                                                "business_name"
                                            ] = edited_business_name

                                            current_result[
                                                "business_type"
                                            ] = edited_business_type

                                            st.session_state[
                                                "website_builder_result"
                                            ] = current_result

                                    st.success(
                                        "Website details updated successfully."
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        update_result.get(
                                            "message",
                                            "Unable to update website details.",
                                        )
                                    )
    # ======================================================
    # GET RESULTs
    # ======================================================

    result = st.session_state.get(
        "website_builder_result"
    )

    if not result:

        return

    # ======================================================
    # RESULT
    # ======================================================

    st.divider()

    st.subheader(
        "📊 Website Generation Result"
    )

    # ======================================================
    # METRICS
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Website JSON",
            "Generated ✅",
        )

    with col2:

        st.metric(
            "React Code",
            "Generated ✅",
        )

    with col3:

        guardrail = result.get(
            "guardrail",
            {},
        )

        st.metric(
            "Guardrail",
            "Passed ✅"
            if guardrail.get("valid")
            else "Failed ❌",
        )

    # ======================================================
    # PROJECT FOLDER
    # ======================================================

    folder = result.get(
        "folder"
    )

    if folder:

        st.info(
            f"📁 Project created: `{folder}`"
        )

    # ======================================================
    # CHANGE STATUS
    # ======================================================

    has_changes = st.session_state.get(
        "website_has_unsaved_changes",
        False
    )

    if has_changes:

        st.warning(
            "🟡 This website has changes that are not published yet."
        )

    else:

        st.success(
            "🟢 Website files are synchronized with the current publish state."
        )

    # ======================================================
    # LIVE PREVIEW
    # ======================================================

    st.divider()

    st.subheader(
        "🌐 Live Website Preview"
    )

    if not folder:

        st.warning(
            "Website project folder is not available."
        )

    else:

        preview_state = st.session_state.get(
            "website_live_preview"
        )

        # --------------------------------------------------
        # RUNNING
        # --------------------------------------------------

        if (
            preview_state
            and preview_state.get("success")
        ):

            st.success(
                "🟢 Live website preview is running."
            )

            preview_url = preview_state.get(
                "url"
            )

            preview_port = preview_state.get(
                "port"
            )

            process_id = preview_state.get(
                "pid"
            )

            if preview_url:

                st.link_button(
                    "🌐 Open Live Preview",
                    preview_url,
                    use_container_width=True,
                )

                st.caption(
                    f"Preview URL: `{preview_url}`"
                )

            if preview_port:

                st.caption(
                    f"Port: `{preview_port}`"
                )

            if st.button(
                "🛑 Stop Preview Server",
                use_container_width=True,
                key="stop_website_preview",
            ):

                if process_id:

                    stop_result = stop_preview_server(
                        process_id
                    )

                    if stop_result.get(
                        "success"
                    ):

                        st.session_state.pop(
                            "website_live_preview",
                            None
                        )

                        st.success(
                            "Preview server stopped."
                        )

                        st.rerun()

                    else:

                        st.error(
                            stop_result.get(
                                "message",
                                "Unable to stop preview server.",
                            )
                        )

                else:

                    st.session_state.pop(
                        "website_live_preview",
                        None
                    )

                    st.rerun()

        # --------------------------------------------------
        # NOT RUNNING
        # --------------------------------------------------

        else:

            st.info(
                "Website is generated. Start the live preview to inspect the current files."
            )

            if st.button(
                "🚀 Start Live Website Preview",
                use_container_width=True,
                key="start_website_preview",
            ):

                with st.spinner(
                    "🌐 Starting website preview..."
                ):

                    preview_result = start_preview_server(
                        folder
                    )

                if preview_result.get(
                    "success"
                ):

                    st.session_state[
                        "website_live_preview"
                    ] = preview_result

                    st.success(
                        "✅ Live website preview started!"
                    )

                    st.rerun()

                else:

                    st.error(
                        preview_result.get(
                            "message",
                            "Unable to start website preview.",
                        )
                    )

                    preview_error = preview_result.get(
                        "error"
                    )

                    if preview_error:

                        st.code(
                            str(preview_error),
                            language="text",
                        )
    
    # ======================================================
    # WEBSITE EDITOR
    # ======================================================

    if folder:

        st.divider()

        st.subheader(
            "✏️ Website Editor"
        )

        st.caption(
            "Make controlled changes to the existing website without regenerating the entire project."
        )

        # --------------------------------------------------
        # INSPECT
        # --------------------------------------------------

        with st.expander(
            "🔍 Website Information",
            expanded=False,
        ):

            if st.button(
                "📋 Inspect Website",
                use_container_width=True,
                key="inspect_website_editor",
            ):

                with st.spinner(
                    "🔍 Inspecting website..."
                ):

                    summary = get_edit_summary(
                        folder
                    )

                if summary.get(
                    "success"
                ):

                    st.success(
                        "Website structure inspected successfully."
                    )

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:

                        st.metric(
                            "Source Files",
                            summary.get(
                                "files",
                                0
                            )
                        )

                    with info_col2:

                        st.metric(
                            "Characters",
                            f"{summary.get('characters', 0):,}"
                        )

                    if summary.get(
                        "main_app"
                    ):

                        st.caption(
                            f"Main React: `{summary['main_app']}`"
                        )

                    if summary.get(
                        "main_css"
                    ):

                        st.caption(
                            f"Main CSS: `{summary['main_css']}`"
                        )

                else:

                    st.error(
                        summary.get(
                            "message",
                            "Unable to inspect website."
                        )
                    )
                # --------------------------------------------------
        # AI WEBSITE EDITOR
        # --------------------------------------------------

        st.markdown(
            "### ✨ AI Website Editor"
        )

        st.caption(
            "Describe the change you want, and AI will create and apply a safe website edit."
        )

        ai_edit_request = st.text_area(
            "What would you like to change?",
            placeholder=(
                "Examples:\n"
                "- Change all BOOK APPOINTMENT buttons to BOOK NOW\n"
                "- Make all buttons more rounded\n"
                "- Change the hero heading"
            ),
            height=140,
            key="website_ai_edit_request",
        )

        if st.button(
            "✨ Apply AI Edit",
            use_container_width=True,
            key="website_apply_ai_edit",
        ):

            if not ai_edit_request.strip():

                st.warning(
                    "Please describe the change you want."
                )

            else:

                with st.spinner(
                    "🤖 AI is understanding and applying your website change..."
                ):

                    try:

                        edit_result = execute_ai_edit(
                            folder,
                            ai_edit_request.strip(),
                        )

                    except Exception as e:

                        edit_result = {

                            "success": False,

                            "message":
                                "AI website editing failed.",

                            "error":
                                str(e),

                        }

                if edit_result.get(
                    "success"
                ):

                    _mark_website_changed()

                    st.session_state[
                        "website_edit_result"
                    ] = edit_result

                    st.success(
                        edit_result.get(
                            "message",
                            "Website updated successfully.",
                        )
                    )

                    edited_file = edit_result.get(
                        "file"
                    )

                    replacements = edit_result.get(
                        "replacements"
                    )

                    if edited_file:

                        st.caption(
                            f"Edited file: `{edited_file}`"
                        )

                    if replacements is not None:

                        st.caption(
                            f"Changes applied: {replacements}"
                        )

                    plan = edit_result.get(
                        "plan"
                    )

                    if plan:

                        with st.expander(
                            "🧠 AI Edit Plan"
                        ):

                            st.json(
                                plan
                            )

                    st.info(
                        "💾 A backup was created before the website was modified."
                    )

                    st.success(
                        "🎉 AI edit completed. Restart the preview to see the updated website."
                    )

                    st.rerun()

                else:

                    st.error(
                        edit_result.get(
                            "message",
                            "Unable to apply AI website edit.",
                        )
                    )

                    edit_error = edit_result.get(
                        "error"
                    )

                    if edit_error:

                        st.code(
                            str(edit_error),
                            language="text",
                        )

                    plan = edit_result.get(
                        "plan"
                    )

                    if plan:

                        with st.expander(
                            "🧠 AI Edit Plan"
                        ):

                            st.json(
                                plan
                            )
        # --------------------------------------------------
        # TEXT EDITOR
        # --------------------------------------------------

        st.markdown(
            "### 📝 Replace Website Text"
        )

        st.caption(
            "Use this when you know the exact existing text and want to replace it."
        )

        old_text = st.text_area(
            "Existing Text",
            placeholder=(
                "Example:\n"
                "Your Smile, Our Priority"
            ),
            height=100,
            key="website_editor_old_text",
        )

        new_text = st.text_area(
            "New Text",
            placeholder=(
                "Example:\n"
                "A Healthier Smile Starts Here"
            ),
            height=100,
            key="website_editor_new_text",
        )

        if st.button(
            "💾 Apply Text Change",
            use_container_width=True,
            key="website_editor_replace_text",
        ):

            if not old_text.strip():

                st.warning(
                    "Please enter the existing text."
                )

            elif not new_text.strip():

                st.warning(
                    "Please enter the new text."
                )

            elif old_text == new_text:

                st.warning(
                    "Existing text and new text are identical."
                )

            else:

                with st.spinner(
                    "✏️ Applying text change..."
                ):

                    edit_result = edit_website(

                        folder,

                        "replace_text",

                        old_text=old_text,

                        new_text=new_text,
                    )

                if edit_result.get(
                    "success"
                ):

                    _mark_website_changed()

                    st.session_state[
                        "website_edit_result"
                    ] = edit_result

                    st.success(
                        "✅ Text changed successfully. A backup was created before the change."
                    )

                    st.rerun()

                else:

                    st.error(
                        edit_result.get(
                            "message",
                            "Unable to change website text.",
                        )
                    )

                    edit_error = edit_result.get(
                        "error"
                    )

                    if edit_error:

                        st.code(
                            str(edit_error),
                            language="text",
                        )

        # --------------------------------------------------
        # CSS EDITOR
        # --------------------------------------------------

        st.markdown(
            "### 🎨 Custom CSS"
        )

        st.caption(
            "Append additional CSS styles to customize the current website."
        )

        css_code = st.text_area(
            "CSS",
            placeholder=(
                "Example:\n\n"
                ".hero-title {\n"
                "    letter-spacing: -0.02em;\n"
                "}\n"
            ),
            height=220,
            key="website_editor_css",
        )

        if st.button(
            "🎨 Apply CSS Changes",
            use_container_width=True,
            key="website_editor_append_css",
        ):

            if not css_code.strip():

                st.warning(
                    "Please enter CSS code."
                )

            else:

                with st.spinner(
                    "🎨 Applying CSS changes..."
                ):

                    edit_result = edit_website(

                        folder,

                        "append_css",

                        css=css_code,
                    )

                if edit_result.get(
                    "success"
                ):

                    _mark_website_changed()

                    st.session_state[
                        "website_edit_result"
                    ] = edit_result

                    st.success(
                        "✅ CSS changes applied. A backup was created before the change."
                    )

                    st.rerun()

                else:

                    st.error(
                        edit_result.get(
                            "message",
                            "Unable to apply CSS changes.",
                        )
                    )

                    edit_error = edit_result.get(
                        "error"
                    )

                    if edit_error:

                        st.code(
                            str(edit_error),
                            language="text",
                        )

        # --------------------------------------------------
        # LAST EDIT RESULT
        # --------------------------------------------------

        edit_result = st.session_state.get(
            "website_edit_result"
        )

        if edit_result:

            with st.expander(
                "📋 Last Edit Result",
                expanded=False,
            ):

                st.json(
                    edit_result
                )

        # --------------------------------------------------
        # IMPORTANT WORKFLOW INFO
        # --------------------------------------------------

        st.info(
            "💡 After editing, start the preview again to inspect the changes. "
            "When satisfied, use 'Update Live Website' below to publish them."
        )

    # ======================================================
    # PUBLISH WEBSITE
    # ======================================================

    st.divider()

    st.subheader(
        "🚀 Publish Website"
    )

    st.caption(
        "Build the website for production and publish it live on Netlify."
    )

    publish_result = st.session_state.get(
        "website_publish_result"
    )

    # ======================================================
    # PUBLISHED WEBSITE
    # ======================================================

    if (
        publish_result
        and publish_result.get("success")
    ):

        live_url = publish_result.get(
            "live_url"
        )

        admin_url = publish_result.get(
            "admin_url"
        )

        st.success(
            "🟢 Website is live!"
        )

        if live_url:

            live_col, admin_col = st.columns(
                2
            )

            with live_col:

                st.link_button(
                    "Open Live Website",
                    live_url,
                    use_container_width=True,
                )

            with admin_col:

                if admin_url:

                    st.link_button(
                        "Open Netlify Dashboard",
                        admin_url,
                        use_container_width=True,
                    )

        site_id = publish_result.get(
            "site_id"
        )

        deploy_id = publish_result.get(
            "deploy_id"
        )

        if site_id:

            st.caption(
                f"Netlify Site ID: `{site_id}`"
            )

        if deploy_id:

            st.caption(
                f"Deployment ID: `{deploy_id}`"
            )

    # ======================================================
    # PUBLISH / UPDATE
    # ======================================================

    if has_changes:

        button_label = (
            "🚀 Publish Changes Live"
        )

    elif (
        publish_result
        and publish_result.get("success")
    ):

        button_label = (
            "🔄 Update Live Website"
        )

    else:

        button_label = (
            "🚀 Publish Website Live"
        )

    if st.button(
        button_label,
        use_container_width=True,
        key="website_publish",
    ):

        if not folder:

            st.error(
                "Website project folder is not available."
            )

        else:

            with st.spinner(
                "🚀 Building and publishing website..."
            ):

                publish_response = publish_website(

                    folder,

                    business_name.strip(),
                )

        if publish_response.get(
            "success"
            ):

                # ------------------------------------------
                # SAVE PUBLISH RESULT
                # ------------------------------------------

                st.session_state[
                    "website_publish_result"
                ] = publish_response

                # ------------------------------------------
                # SYNC PUBLISHED WEBSITE WITH DATABASE
                # ------------------------------------------

                current_website_id = (
                    st.session_state.get(
                        "current_website_id"
                    )
                    or result.get(
                        "website_id"
                    )
                )

                current_user_data = current_user()

                current_user_id = (
                    current_user_data.get("id")
                    if current_user_data
                    else None
                )

                if (
                    current_website_id
                    and current_user_id
                ):

                    update_fields = {

                        "status": "published",

                        "live_url":
                            publish_response.get(
                                "live_url"
                            ),

                    }

                    site_id = publish_response.get(
                        "site_id"
                    )

                    if site_id:

                        update_fields[
                            "netlify_site_id"
                        ] = site_id

                    database_update = (
                        update_website_record(
                            current_website_id,
                            user_id=current_user_id,
                            **update_fields,
                        )
                    )

                    if not database_update.get(
                        "success"
                    ):

                        st.warning(
                            "Website was published, but "
                            "the account record could not "
                            "be updated."
                        )

                    else:

                        result[
                            "website_id"
                        ] = current_website_id

                        result[
                            "live_url"
                        ] = publish_response.get(
                            "live_url"
                        )

                        result[
                            "status"
                        ] = "published"

                        st.session_state[
                            "website_builder_result"
                        ] = result

                        st.session_state[
                            "current_website_id"
                        ] = current_website_id
                # ------------------------------------------
                # CLEAR UNSAVED CHANGES
                # ------------------------------------------

                st.session_state[
                    "website_has_unsaved_changes"
                ] = False

                st.success(
                    "🎉 Website published successfully!"
                )

                st.rerun()
        else:

                st.error(
                    publish_response.get(
                        "message",
                        "Unable to publish website.",
                    )
                )

                publish_error = publish_response.get(
                    "error"
                )

                if publish_error:

                    st.code(
                        str(publish_error),
                        language="text",
                    )

    # ======================================================
    # WEBSITE FILE PREVIEW
    # ======================================================

    if folder:

        st.divider()

        show_preview(
            folder
        )

    # ======================================================
    # REACT CODE
    # ======================================================

    react_code = result.get(
        "react_code"
    )

    if react_code:

        st.divider()

        with st.expander(
            "💻 View Generated React Code"
        ):

            st.code(
                react_code,
                language="jsx",
            )

    # ======================================================
    # WEBSITE JSON
    # ======================================================

    website_json = result.get(
        "json"
    )

    if website_json:

        with st.expander(
            "🧩 View Website Data"
        ):

            st.json(
                website_json
            )

    # ======================================================
    # GUARDRAIL
    # ======================================================

    guardrail = result.get(
        "guardrail"
    )

    if guardrail:

        st.divider()

        if guardrail.get(
            "valid"
        ):

            st.success(
                "🛡️ Website Guardrail Passed — no unsupported business claims detected."
            )

        else:

            st.error(
                "🛡️ Website Guardrail Failed."
            )

            matches = guardrail.get(
                "matches",
                []
            )

            if matches:

                st.write(
                    "Detected:",
                    ", ".join(
                        matches
                    ),
                )