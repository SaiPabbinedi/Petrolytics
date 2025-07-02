# utils.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(uploaded_file):
    """
    Loads data from an uploaded CSV or Excel file into a pandas DataFrame.
    This function is cached, so data is only read once per unique file upload.
    """
    if uploaded_file is None:
        return None

    # st.info(f"Loading data from {uploaded_file.name} (this message appears only if not cached)...")
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type.")
        return None
    return df