import streamlit as st
import pandas as pd


def show_overview(original_df, cleaned_df, summary):
    """
    Displays the Overview page.

    Parameters
    ----------
    original_df : pandas.DataFrame
        Original uploaded dataset.

    cleaned_df : pandas.DataFrame
        Cleaned dataset.

    summary : dict
        Cleaning summary returned by clean_data().
    """

    st.header("📊 Dataset Overview")

    st.write(
        "This section provides a quick overview of the uploaded dataset "
        "before and after cleaning."
    )

    st.markdown("---")

    # ==========================================================
    # Dataset Metrics
    # ==========================================================

    st.subheader("📌 Dataset Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Rows",
            value=summary["original_rows"]
        )

    with col2:
        st.metric(
            label="Columns",
            value=summary["original_columns"]
        )

    with col3:
        st.metric(
            label="Missing Values",
            value=summary["missing_before"]
        )

    with col4:
        st.metric(
            label="Duplicates Removed",
            value=summary["duplicates_removed"]
        )

    st.markdown("---")

    # ==========================================================
    # Original Dataset
    # ==========================================================

    st.subheader("📄 Original Dataset Preview")

    st.dataframe(
        original_df.head(20),
        use_container_width=True,
        height=400
    )

    st.caption("Showing first 20 rows of the uploaded dataset.")

    st.markdown("---")

    # ==========================================================
    # Cleaning Summary
    # ==========================================================

    st.subheader("🧹 Cleaning Summary")

    summary_df = pd.DataFrame({

        "Metric": [

            "Original Rows",

            "Original Columns",

            "Missing Values Before Cleaning",

            "Duplicates Removed",

            "Missing Values After Cleaning"

        ],

        "Value": [

            summary["original_rows"],

            summary["original_columns"],

            summary["missing_before"],

            summary["duplicates_removed"],

            summary["missing_after"]

        ]

    })

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ==========================================================
    # Cleaned Dataset
    # ==========================================================

    st.subheader("✅ Cleaned Dataset Preview")

    st.dataframe(
        cleaned_df.head(20),
        use_container_width=True,
        height=400
    )

    st.caption("Showing first 20 rows after automatic data cleaning.")

    st.markdown("---")

    # ==========================================================
    # Data Types
    # ==========================================================

    st.subheader("📌 Column Data Types")

    dtype_df = (
        cleaned_df.dtypes
        .astype(str)
        .reset_index()
    )

    dtype_df.columns = ["Column Name", "Data Type"]

    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ==========================================================
    # Dataset Shape
    # ==========================================================

    st.subheader("📐 Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"Rows : **{cleaned_df.shape[0]}**"
        )

    with col2:
        st.info(
            f"Columns : **{cleaned_df.shape[1]}**"
        )

    st.markdown("---")

    # ==========================================================
    # Memory Usage
    # ==========================================================

    memory = round(
        cleaned_df.memory_usage(deep=True).sum() / (1024 * 1024),
        2
    )

    st.subheader("💾 Memory Usage")

    st.success(
        f"Dataset occupies approximately **{memory} MB** in memory."
    )