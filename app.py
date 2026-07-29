import streamlit as st

from core.startup import startup
from core.initializer import initialize
from core.auth_guard import require_login
from core.router import run


# =========================
# Application Startup
# =========================

startup()

initialize()

require_login()

run()

st.stop()