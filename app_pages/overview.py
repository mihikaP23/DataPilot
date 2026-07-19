import streamlit as st
import pandas as pd


def show_overview(original_df, cleaned_df, summary):

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

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "This section provides a quick overview of the uploaded dataset "
    )

    st.markdown("---")

    # =====================================================
    # KPI CARDS
    # =====================================================

    rows = cleaned_df.shape[0]
    columns = cleaned_df.shape[1]
    missing = int(cleaned_df.isnull().sum().sum())
    duplicates = int(cleaned_df.duplicated().sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Rows", f"{rows:,}")
    c2.metric("📊 Columns", columns)
    c3.metric("❗ Missing Values", missing)
    c4.metric("📑 Duplicates", duplicates)

    st.markdown("---")

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📌 Dataset Information")

        info = pd.DataFrame(
            {
                "Property": [
                    "Rows",
                    "Columns",
                    "Numeric Columns",
                    "Categorical Columns",
                    "Memory Usage (MB)"
                ],
                "Value": [
                    cleaned_df.shape[0],
                    cleaned_df.shape[1],
                    len(cleaned_df.select_dtypes(include="number").columns),
                    len(cleaned_df.select_dtypes(include=["object", "category"]).columns),
                    round(
                        cleaned_df.memory_usage(deep=True).sum()
                        / (1024 * 1024),
                        2
                    )
                ]
            }
        )

        st.dataframe(
            info,
            width="stretch",
            hide_index=True
        )

    with right:

        st.subheader("🧹 Cleaning Summary")

        st.success(
            f"""
Original Rows : {summary['original_rows']}

Original Columns : {summary['original_columns']}

Duplicates Removed : {summary['duplicates_removed']}

Missing Before : {summary['missing_before']}

Missing After : {summary['missing_after']}
"""
        )

    st.markdown("---")

    # =====================================================
    # COLUMN DETAILS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("🔢 Numeric Columns")

        numeric_cols = cleaned_df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            st.dataframe(
                pd.DataFrame(
                    {"Column Name": numeric_cols}
                ),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No Numeric Columns Found.")

    with c2:

        st.subheader("🔤 Categorical Columns")

        cat_cols = cleaned_df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if cat_cols:

            st.dataframe(
                pd.DataFrame(
                    {"Column Name": cat_cols}
                ),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No Categorical Columns Found.")

    st.markdown("---")

    # =====================================================
    # DATA PREVIEW
    # =====================================================

    st.subheader("👀 Cleaned Dataset Preview")

    st.dataframe(
        cleaned_df.head(10),
        width="stretch",
        height=350
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

✅ Data Cleaned

✅ Ready for EDA

✅ Ready for Dashboard

✅ Ready for AI Insights

✅ Ready for Forecasting

✅ Ready for PDF Report
"""
    )