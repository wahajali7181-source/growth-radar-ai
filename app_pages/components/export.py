import streamlit as st


def export_csv(df):

    if df.empty:
        return

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        "📥 Download CSV",

        data=csv,

        file_name="growth_radar_leads.csv",

        mime="text/csv",

        use_container_width=True,

    )