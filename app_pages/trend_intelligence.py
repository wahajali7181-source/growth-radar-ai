import streamlit as st

from auth.session import require_auth
from trend_radar.analyzer import (
    analyze_trends,
    get_trend_summary,
    calculate_trend_score,
    get_opportunity_label,
)
from trend_radar.youtube_engine import get_top_videos


# ==========================================================
# HELPERS
# ==========================================================

def format_number(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return "0"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if value >= 1_000:
        return f"{value / 1_000:.1f}K"

    return str(value)


# ==========================================================
# PAGE
# ==========================================================

def show():

    require_auth()

    st.title("📈 Trend Intelligence")

    st.caption(
        "Discover rising trends using Google Trends and YouTube data."
    )

    st.divider()

    # ======================================================
    # SEARCH
    # ======================================================

    st.subheader("🔎 Analyze a Trend")

    keyword = st.text_input(
        "Enter a keyword or topic",
        placeholder="e.g. AI tools, fitness, Shopify, video editing",
        key="trend_keyword",
    )

    analyze_button = st.button(
        "🚀 Analyze Trend",
        key="trend_analyze_button",
        use_container_width=True,
    )

    # ======================================================
    # ANALYSIS
    # ======================================================

    if analyze_button:

        if not keyword.strip():

            st.warning(
                "Please enter a keyword or topic."
            )

            return

        with st.spinner(
            f"Analyzing '{keyword.strip()}'..."
        ):

            try:

                trend_df = analyze_trends(
                    keyword.strip()
                )

                if trend_df.empty:

                    st.warning(
                        "No Google Trends data was found for this keyword."
                    )

                    return

                summary = get_trend_summary(
                    trend_df
                )

                opportunity_score = calculate_trend_score(
                    summary
                )

                opportunity_label = get_opportunity_label(
                    opportunity_score
                )

                try:

                    videos = get_top_videos(
                        keyword.strip(),
                        6
                    )

                    youtube_error = None

                except Exception as exc:

                    videos = []

                    youtube_error = str(exc)

                # Store results in session state
                st.session_state[
                    "trend_analysis_result"
                ] = {

                    "keyword": keyword.strip(),

                    "trend_df": trend_df,

                    "summary": summary,

                    "opportunity_score":
                        opportunity_score,

                    "opportunity_label":
                        opportunity_label,

                    "videos": videos,

                    "youtube_error":
                        youtube_error,
                }

            except Exception as exc:

                st.error(
                    "Trend analysis failed."
                )

                st.caption(
                    str(exc)
                )

                return

    # ======================================================
    # LOAD SAVED RESULT
    # ======================================================

    result = st.session_state.get(
        "trend_analysis_result"
    )

    if not result:

        st.info(
            "Enter a keyword above and click "
            "**Analyze Trend** to begin."
        )

        return

    trend_df = result["trend_df"]

    summary = result["summary"]

    opportunity_score = result[
        "opportunity_score"
    ]

    opportunity_label = result[
        "opportunity_label"
    ]

    videos = result["videos"]

    youtube_error = result[
        "youtube_error"
    ]

    # ======================================================
    # RESULT HEADER
    # ======================================================

    st.divider()

    st.subheader(
        f"📊 Analysis: {result['keyword']}"
    )

    # ======================================================
    # METRICS
    # ======================================================

    col1, col2, col3, col4, col5 = st.columns(
        5
    )

    with col1:

        st.metric(
            "Current",
            f"{summary['current']:.0f}",
        )

    with col2:

        st.metric(
            "Average",
            f"{summary['average']:.1f}",
        )

    with col3:

        st.metric(
            "Peak",
            f"{summary['peak']:.0f}",
        )

    with col4:

        change = summary[
            "change_percent"
        ]

        st.metric(
            "Change",
            f"{change:+.2f}%",
        )

    with col5:

        st.metric(
            "Opportunity",
            f"{opportunity_score:.1f}/100",
        )

    st.write("")

    # ======================================================
    # STATUS
    # ======================================================

    status_col, opportunity_col = st.columns(
        2
    )

    with status_col:

        st.markdown(
            f"### Trend Status\n"
            f"**{summary['status']}**"
        )

    with opportunity_col:

        st.markdown(
            f"### Opportunity\n"
            f"**{opportunity_label}**"
        )

    # ======================================================
    # GOOGLE TRENDS CHART
    # ======================================================

    st.divider()

    st.subheader(
        "📈 Google Trends — Last 12 Months"
    )

    chart_df = trend_df.copy()

    chart_df = chart_df.set_index(
        "date"
    )

    st.line_chart(
        chart_df[
            ["trend_score"]
        ],
        use_container_width=True,
    )

    # ======================================================
    # TREND DETAILS
    # ======================================================

    st.subheader(
        "📌 Trend Overview"
    )

    detail_col1, detail_col2, detail_col3 = st.columns(
        3
    )

    with detail_col1:

        st.metric(
            "Highest Interest",
            f"{summary['peak']:.0f}",
        )

    with detail_col2:

        st.metric(
            "Lowest Interest",
            f"{summary['lowest']:.0f}",
        )

    with detail_col3:

        st.metric(
            "Trend Direction",
            summary["status"],
        )

    # ======================================================
    # YOUTUBE
    # ======================================================

    st.divider()

    st.subheader(
        "🎥 YouTube Market Activity"
    )

    if youtube_error:

        st.warning(
            "YouTube data could not be loaded."
        )

        st.caption(
            youtube_error
        )

    elif not videos:

        st.info(
            "No YouTube videos were found."
        )

    else:

        st.caption(
            f"Top videos related to "
            f"'{result['keyword']}'"
        )

        for index, video in enumerate(
            videos,
            start=1
        ):

            title = video.get(
                "title",
                "Untitled video"
            )

            channel = video.get(
                "channel",
                "Unknown channel"
            )

            views = video.get(
                "views",
                0
            )

            likes = video.get(
                "likes",
                0
            )

            comments = video.get(
                "comments",
                0
            )

            published = video.get(
                "published",
                ""
            )

            thumbnail = video.get(
                "thumbnail"
            )

            link = video.get(
                "link"
            )

            with st.container(
                border=True
            ):

                video_col1, video_col2 = st.columns(
                    [1, 3]
                )

                with video_col1:

                    if thumbnail:

                        st.image(
                            thumbnail,
                            use_container_width=True,
                        )

                with video_col2:

                    st.markdown(
                        f"### {index}. {title}"
                    )

                    st.caption(
                        f"📺 {channel}"
                    )

                    metric1, metric2, metric3 = st.columns(
                        3
                    )

                    with metric1:

                        st.write(
                            f"👁️ **{format_number(views)}** views"
                        )

                    with metric2:

                        st.write(
                            f"👍 **{format_number(likes)}** likes"
                        )

                    with metric3:

                        st.write(
                            f"💬 **{format_number(comments)}** comments"
                        )

                    if published:

                        st.caption(
                            f"Published: {published}"
                        )

                    if link:

                        st.link_button(
                            "▶ Watch on YouTube",
                            link,
                        )

    # ======================================================
    # RAW DATA
    # ======================================================

    st.divider()

    with st.expander(
        "🧾 View Google Trends Data"
    ):

        st.dataframe(
            trend_df,
            use_container_width=True,
            hide_index=True,
        )