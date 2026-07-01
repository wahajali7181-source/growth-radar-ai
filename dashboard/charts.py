import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_lead_score_chart(df: pd.DataFrame):

    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(6, 3.5))

    ax.hist(
        df["lead_score"],
        bins=5
    )

    ax.set_title("Lead Score Distribution")

    ax.set_xlabel("Lead Score")

    ax.set_ylabel("Businesses")

    st.pyplot(fig)