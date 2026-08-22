import streamlit as st

from auth.session import require_auth
from social_checker.checker import check_socials
from social_checker.analyzer import analyze_social_presence


def show():

    # ==========================================================
    # AUTH
    # ==========================================================

    require_auth()

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title("📱 Social Intelligence")

    st.caption(
        "Analyze a business's social media presence, contact information, "
        "strengths, weaknesses, and growth opportunities."
    )

    st.divider()

    # ==========================================================
    # SELECTED BUSINESS
    # ==========================================================

    selected_business = st.session_state.get(
        "selected_business"
    )

    if selected_business:

        business_name = str(
            selected_business.get(
                "name",
                "Selected Business"
            )
        )

        business_website = str(
            selected_business.get(
                "website",
                ""
            )
        ).strip()

        st.subheader(
            "🎯 Selected Business"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Business:** {business_name}"
            )

        with c2:

            st.write(
                f"**Website:** "
                f"{business_website or 'Not Available'}"
            )

        if business_website:

            if st.button(
                "🔎 Analyze Selected Lead",
                use_container_width=True,
                key="analyze_selected_social"
            ):

                st.session_state[
                    "social_analysis_website"
                ] = business_website

                st.session_state[
                    "run_selected_social_analysis"
                ] = True

                st.rerun()

        else:

            st.warning(
                "This selected business does not have a website. "
                "Use the manual analyzer below."
            )

    else:

        st.info(
            "No business is currently selected. "
            "You can analyze a website manually below."
        )

    st.divider()

    # ==========================================================
    # MANUAL WEBSITE ANALYSIS
    # ==========================================================

    st.subheader(
        "🌐 Analyze Website"
    )

    default_website = st.session_state.get(
        "social_analysis_website",
        ""
    )

    website = st.text_input(
        "Business Website",
        value=default_website,
        placeholder="example.com",
        key="social_website_input"
    )

    manual_analysis_clicked = st.button(
        "🚀 Analyze Social Presence",
        use_container_width=True,
        key="analyze_social_button"
    )

    selected_analysis_clicked = st.session_state.pop(
        "run_selected_social_analysis",
        False
    )

    # Run either manual analysis or selected-business analysis
    if manual_analysis_clicked or selected_analysis_clicked:

        analysis_website = (
            website.strip()
            if manual_analysis_clicked
            else st.session_state.get(
                "social_analysis_website",
                website.strip()
            )
        )

        if not analysis_website:

            st.warning(
                "Please enter a business website."
            )

            return

        with st.spinner(
            "🔍 Analyzing social presence..."
        ):

            try:

                result = check_socials(
                    analysis_website
                )

                analysis = analyze_social_presence(
                    result
                )

            except Exception as e:

                st.error(
                    f"❌ Social Intelligence Error: {e}"
                )

                return

        # ======================================================
        # SAVE ANALYSIS
        # ======================================================

        st.session_state[
            "social_analysis_result"
        ] = result

        st.session_state[
            "social_analysis_summary"
        ] = analysis

        st.session_state[
            "social_analysis_website"
        ] = analysis_website

        # ======================================================
        # CONNECT WITH SELECTED BUSINESS
        # ======================================================

        if selected_business:

            selected_business[
                "social_score"
            ] = analysis.get(
                "score",
                0
            )

            selected_business[
                "social_status"
            ] = analysis.get(
                "status",
                "Unknown"
            )

            selected_business[
                "social_analysis"
            ] = str(
                analysis
            )

            selected_business[
                "social_strengths"
            ] = " | ".join(
                analysis.get(
                    "strengths",
                    []
                )
            )

            selected_business[
                "social_weaknesses"
            ] = " | ".join(
                analysis.get(
                    "weaknesses",
                    []
                )
            )

            selected_business[
                "social_recommendations"
            ] = " | ".join(
                analysis.get(
                    "recommendations",
                    []
                )
            )

            selected_business[
                "missing_social_platforms"
            ] = " | ".join(
                analysis.get(
                    "missing_platforms",
                    []
                )
            )

            # --------------------------------------------------
            # SOCIAL PLATFORMS
            # --------------------------------------------------

            social_platforms = [
                "instagram",
                "facebook",
                "linkedin",
                "youtube",
                "tiktok",
                "twitter"
            ]

            for platform in social_platforms:

                selected_business[
                    platform
                ] = result.get(
                    platform,
                    ""
                )

            # --------------------------------------------------
            # CONTACT INFORMATION
            # --------------------------------------------------

            contact_fields = [
                "email",
                "phone",
                "whatsapp",
                "google_maps"
            ]

            for field in contact_fields:

                selected_business[
                    field
                ] = result.get(
                    field,
                    ""
                )

            # Save updated business
            st.session_state[
                "selected_business"
            ] = selected_business

        st.success(
            "✅ Social Intelligence analysis completed."
        )

    # ==========================================================
    # DISPLAY RESULTS
    # ==========================================================

    result = st.session_state.get(
        "social_analysis_result"
    )

    analysis = st.session_state.get(
        "social_analysis_summary"
    )

    if not result or not analysis:

        return

    st.divider()

    st.subheader(
        "📊 Social Intelligence Report"
    )

    # ==========================================================
    # SCORE
    # ==========================================================

    score = analysis.get(
        "score",
        0
    )

    status = analysis.get(
        "status",
        "Unknown"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Social Score",
            f"{score}/100"
        )

    with c2:

        st.metric(
            "Status",
            status
        )

    st.divider()

    # ==========================================================
    # SOCIAL PLATFORMS
    # ==========================================================

    st.subheader(
        "🌐 Social Platforms"
    )

    platforms = [

        ("instagram", "📸 Instagram"),

        ("facebook", "📘 Facebook"),

        ("linkedin", "💼 LinkedIn"),

        ("youtube", "▶️ YouTube"),

        ("tiktok", "🎵 TikTok"),

        ("twitter", "𝕏 Twitter"),

    ]

    for key, label in platforms:

        value = result.get(
            key,
            ""
        )

        if value and "Not Found" not in str(value):

            st.success(
                f"{label}: {value}"
            )

        else:

            st.error(
                f"{label}: Not Found"
            )

    st.divider()

    # ==========================================================
    # CONTACT INFORMATION
    # ==========================================================

    st.subheader(
        "📞 Contact Information"
    )

    contact_fields = [

        ("website", "🌐 Website"),

        ("email", "📧 Email"),

        ("phone", "📞 Phone"),

        ("whatsapp", "💬 WhatsApp"),

        ("google_maps", "📍 Google Maps"),

    ]

    contact_columns = st.columns(2)

    index = 0

    for key, label in contact_fields:

        value = result.get(
            key,
            ""
        )

        with contact_columns[
            index % 2
        ]:

            if (
                value
                and "Not Found"
                not in str(value)
            ):

                st.success(
                    f"**{label}**\n\n{value}"
                )

            else:

                st.warning(
                    f"**{label}**\n\nNot Found"
                )

        index += 1

    st.divider()

    # ==========================================================
    # STRENGTHS
    # ==========================================================

    st.subheader(
        "💪 Strengths"
    )

    strengths = analysis.get(
        "strengths",
        []
    )

    if strengths:

        for strength in strengths:

            st.success(
                f"✅ {strength}"
            )

    else:

        st.info(
            "No major strengths detected."
        )

    # ==========================================================
    # WEAKNESSES
    # ==========================================================

    st.subheader(
        "⚠️ Weaknesses"
    )

    weaknesses = analysis.get(
        "weaknesses",
        []
    )

    if weaknesses:

        for weakness in weaknesses:

            st.warning(
                f"⚠️ {weakness}"
            )

    else:

        st.success(
            "No major weaknesses detected."
        )

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    st.subheader(
        "💡 Recommendations"
    )

    recommendations = analysis.get(
        "recommendations",
        []
    )

    if recommendations:

        for recommendation in recommendations:

            st.info(
                f"💡 {recommendation}"
            )

    else:

        st.success(
            "No additional recommendations."
        )

    # ==========================================================
    # MISSING PLATFORMS
    # ==========================================================

    missing_platforms = analysis.get(
        "missing_platforms",
        []
    )

    if missing_platforms:

        st.divider()

        st.subheader(
            "📌 Missing Platforms"
        )

        st.write(
            ", ".join(
                missing_platforms
            )
        )

    # ==========================================================
    # AI EMPLOYEE CONNECTION
    # ==========================================================

    if selected_business:

        st.divider()

        st.subheader(
            "🤖 AI Employee"
        )

        st.success(
            "Social Intelligence data has been connected "
            "to the selected business."
        )

        st.caption(
            "Open AI Employees → AI Social Media Manager "
            "to generate a strategy using this analysis."
        )