import streamlit as st

from src.common import *

params = page_setup(page="main")


st.markdown(
    """# OpenPepXL

Streamlit interface for OpenPepXL."""
)

save_params(params)
