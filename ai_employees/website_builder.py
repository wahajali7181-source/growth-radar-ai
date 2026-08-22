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
            "✅ Website generated successfully!"
        )

        st.rerun()

    # ======================================================
    # GET RESULT
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

            st.markdown(
                "### 🌐 Live Website"
            )

            st.code(
                live_url,
                language="text",
            )

            st.link_button(
                "🌐 Open Live Website",
                live_url,
                use_container_width=True,
            )

        if admin_url:

            st.link_button(
                "⚙️ Open Netlify Dashboard",
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

                st.session_state[
                    "website_publish_result"
                ] = publish_response

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