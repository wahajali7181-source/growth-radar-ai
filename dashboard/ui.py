import streamlit as st


def show_dashboard_cards(metrics):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "🏢 Businesses",
            metrics["businesses"]
        )

    with col2:
        st.metric(
            "🎯 Qualified",
            metrics["qualified"]
        )

    with col3:
        st.metric(
            "⭐ Avg Score",
            metrics["average_score"]
        )

    with col4:
        st.metric(
            "🔥 High Opp.",
            metrics["high_opportunity"]
        )

    with col5:
        st.metric(
            "💰 Revenue",
            f"${metrics['estimated_revenue']:,}"
        )