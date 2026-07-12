import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ==========================
           APP
        ========================== */

        .stApp{
            background:#0f172a;
            color:white;
        }

        /* ==========================
           SIDEBAR
        ========================== */

        section[data-testid="stSidebar"]{
            background:#111827;
            border-right:1px solid #2d3748;
        }

        /* ==========================
           BUTTONS
        ========================== */

        .stButton>button{

            background:linear-gradient(90deg,#2563eb,#06b6d4);

            color:white;

            border:none;

            border-radius:12px;

            padding:12px 24px;

            font-weight:600;

            transition:0.3s;
        }

        .stButton>button:hover{

            transform:translateY(-2px);

            box-shadow:0 0 20px rgba(37,99,235,.4);
        }

        /* ==========================
           METRICS
        ========================== */

        div[data-testid="stMetric"]{

            background:#1e293b;

            border-radius:15px;

            padding:15px;

            border:1px solid #334155;
        }

        /* ==========================
           DATAFRAME
        ========================== */

        div[data-testid="stDataFrame"]{

            border-radius:15px;

            overflow:hidden;
        }

        h1,h2,h3{

            color:white;
        }

        </style>
        """,
        unsafe_allow_html=True
    )