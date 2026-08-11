import streamlit as st


def show_actions(df):

    if df.empty:

        return

    st.subheader("⚡ Bulk Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.button(

            "📄 Generate Proposals",

            use_container_width=True,

            disabled=True,

        )

    with c2:

        st.button(

            "🤖 AI Sales Strategy",

            use_container_width=True,

            disabled=True,

        )

    with c3:

        st.button(

            "📤 Export CSV",

            use_container_width=True,

            disabled=True,

        )

    with c4:

        st.button(

            "📧 Outreach Campaign",

            use_container_width=True,

            disabled=True,

        )