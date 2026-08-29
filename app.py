import streamlit as st

from core.startup import startup
from core.initializer import initialize
from core.router import run


startup()

initialize()

run() 