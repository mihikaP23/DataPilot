import pandas as pd
import streamlit as st


def upload_dataset():
    """
    Upload a CSV or Excel dataset.

    Returns:
        pd.DataFrame | None
    """

    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is None:
        return None

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        return df

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None