
import streamlit as st
import pandas as pd


def show_overview(original_df, cleaned_df, summary):

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg,#2563EB,#1E40AF);
            padding:25px;
            border-radius:15px;
            color:white;
            margin-bottom:25px;
        ">
            <h2 style="color:white;margin-bottom:5px;">
                📊 Dataset Overview
            </h2>
            <p style="color:white;margin:0;">
                Explore your uploaded dataset and preprocessing results.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "This section provides an overview of the original dataset, "
        "its structure, missing values, duplicates and cleaning results."
    )

    st.markdown("---")

    # =====================================================
    # ORIGINAL DATASET STATISTICS
    # =====================================================

    original_rows = original_df.shape[0]
    original_columns = original_df.shape[1]

    original_missing = int(original_df.isnull().sum().sum())
    original_duplicates = int(original_df.duplicated().sum())

    cleaned_rows = cleaned_df.shape[0]
    cleaned_columns = cleaned_df.shape[1]

    cleaned_missing = int(cleaned_df.isnull().sum().sum())
    cleaned_duplicates = int(cleaned_df.duplicated().sum())

    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("📌 Original Dataset Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📄 Total Rows",
        f"{original_rows:,}"
    )

    c2.metric(
        "📊 Total Columns",
        original_columns
    )

    c3.metric(
        "❗ Missing Values",
        f"{original_missing:,}"
    )

    c4.metric(
        "📑 Duplicate Rows",
        f"{original_duplicates:,}"
    )

    st.markdown("---")

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📋 Dataset Information")

        numeric_cols = original_df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = original_df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        datetime_cols = original_df.select_dtypes(
            include=["datetime"]
        ).columns.tolist()

        memory_usage = round(
            original_df.memory_usage(deep=True).sum()
            / (1024 * 1024), 2
        )

        info = pd.DataFrame({
            "Property": [
                "Total Rows",
                "Total Columns",
                "Numeric Columns",
                "Categorical Columns",
                "Datetime Columns",
                "Memory Usage (MB)"
            ],

            "Value": [
                f"{original_rows:,}",
                str(original_columns),
                str(len(numeric_cols)),
                str(len(categorical_cols)),
                str(len(datetime_cols)),
                str(memory_usage)
            ]
        })

        st.dataframe(
            info,
            width="stretch",
            hide_index=True
        )

    with right:

        st.subheader("🧹 Cleaning Summary")

        st.success(
            f"""
**Original Rows:** {summary['original_rows']:,}

**Original Columns:** {summary['original_columns']}

**Duplicates Removed:** {summary['duplicates_removed']:,}

**Missing Before:** {summary['missing_before']:,}

**Missing After:** {summary['missing_after']:,}
"""
        )

    st.markdown("---")

    # =====================================================
    # BEFORE AND AFTER CLEANING
    # =====================================================

    st.subheader("🔄 Before vs After Cleaning")

    b1, b2 = st.columns(2)

    with b1:

        st.markdown("**Original Dataset**")

        st.metric("Rows", f"{original_rows:,}")
        st.metric("Missing Values", f"{original_missing:,}")
        st.metric("Duplicate Rows", f"{original_duplicates:,}")

    with b2:

        st.markdown("**Cleaned Dataset**")

        st.metric("Rows", f"{cleaned_rows:,}")
        st.metric("Missing Values", f"{cleaned_missing:,}")
        st.metric("Duplicate Rows", f"{cleaned_duplicates:,}")

    st.markdown("---")

    # =====================================================
    # MISSING VALUES ANALYSIS
    # =====================================================

    st.subheader("❗ Missing Values Analysis")

    missing_data = original_df.isnull().sum()

    missing_data = missing_data[missing_data > 0]

    if not missing_data.empty:

        missing_table = pd.DataFrame({
            "Column Name": missing_data.index.astype(str),
            "Missing Values": missing_data.values,
            "Missing Percentage": (
                missing_data.values / original_rows * 100
            ).round(2)
        })

        st.dataframe(
            missing_table,
            width="stretch",
            hide_index=True
        )

    else:

        st.success("No missing values found in the original dataset.")

    st.markdown("---")

    # =====================================================
    # COLUMN DETAILS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("🔢 Numeric Columns")

        cleaned_numeric_cols = cleaned_df.select_dtypes(
            include="number"
        ).columns.tolist()

        if cleaned_numeric_cols:

            st.dataframe(
                pd.DataFrame({
                    "Column Name": cleaned_numeric_cols
                }),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No numeric columns found.")

    with c2:

        st.subheader("🔤 Categorical Columns")

        cleaned_cat_cols = cleaned_df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if cleaned_cat_cols:

            st.dataframe(
                pd.DataFrame({
                    "Column Name": cleaned_cat_cols
                }),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No categorical columns found.")

    st.markdown("---")

    # =====================================================
    # ORIGINAL DATASET PREVIEW
    # =====================================================

    st.subheader("👀 Original Dataset Preview")

    st.caption(
        "First 10 rows of the uploaded dataset before preprocessing."
    )

    st.dataframe(
        original_df.head(10),
        width="stretch",
        height=350
    )

    st.markdown("---")

    # =====================================================
    # CLEANED DATASET PREVIEW
    # =====================================================

    st.subheader("🧹 Cleaned Dataset Preview")

    st.caption(
        "First 10 rows after applying data cleaning operations."
    )

    st.dataframe(
        cleaned_df.head(10),
        width="stretch",
        height=350
    )

    st.markdown("---")

    # =====================================================
    # DOWNLOAD CLEANED DATASET
    # =====================================================

    st.subheader("⬇️ Download Cleaned Dataset")

    st.write(
        "Download the preprocessed dataset in CSV format "
        "for further analysis or future use."
    )

    cleaned_csv = cleaned_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=cleaned_csv,
        file_name="AB_NYC_2019_Cleaned.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # PROJECT STATUS
    # =====================================================

    st.subheader("🚀 Analysis Pipeline")

    st.progress(100)

    st.success(
        """
        ✅ Dataset Uploaded

        ✅ Data Cleaning Completed

        ✅ Ready for EDA

        ✅ Ready for AI Insights

        ✅ Ready for PDF Report
        """
    )
