import streamlit as st

from modules.eda import (
    generate_summary,
    statistical_summary,
    missing_values_report,
    correlation_matrix
)


def show_eda(df):
    """
    Displays the Exploratory Data Analysis (EDA) page.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned dataset.
    """

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
                📈 Exploratory Data Analysis (EDA)
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "This section provides descriptive statistics and data quality "
        "analysis of the cleaned dataset."
    )

    st.markdown("---")

    # ==========================================================
    # Dataset Summary
    # ==========================================================

    summary = generate_summary(df)

    st.subheader("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Numeric Columns",
            summary["Numeric Columns"]
        )

    with col2:
        st.metric(
            "Categorical Columns",
            summary["Categorical Columns"]
        )

    with col3:
        st.metric(
            "Datetime Columns",
            summary["Datetime Columns"]
        )

    st.metric(
        "Memory Usage (MB)",
        summary["Memory Usage (MB)"]
    )

    st.markdown("---")

    # ==========================================================
    # Statistical Summary
    # ==========================================================

    st.subheader("📋 Statistical Summary")

    stats = statistical_summary(df)

    st.dataframe(
        stats,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================================
    # Missing Values Report
    # ==========================================================

    st.subheader("❗ Missing Values Report")

    missing = missing_values_report(df)

    if missing.empty:

        st.success("✅ No missing values found after cleaning.")

    else:

        st.dataframe(
            missing,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================================================
    # Correlation Matrix
    # ==========================================================

    st.subheader("📌 Correlation Matrix")

    corr = correlation_matrix(df)

    if corr is not None:

        st.dataframe(
            corr,
            use_container_width=True
        )

    else:

        st.warning(
            "Not enough numeric columns available to compute correlation."
        )

    st.markdown("---")

    # ==========================================================
    # Data Quality Report
    # ==========================================================

    st.subheader("📄 Data Quality Report")

    total_rows = df.shape[0]
    total_columns = df.shape[1]

    duplicate_rows = df.duplicated().sum()

    missing_values = df.isnull().sum().sum()

    numeric_columns = len(df.select_dtypes(include="number").columns)

    categorical_columns = len(df.select_dtypes(include="object").columns)

    report = {
        "Total Rows": total_rows,
        "Total Columns": total_columns,
        "Numeric Columns": numeric_columns,
        "Categorical Columns": categorical_columns,
        "Duplicate Rows": duplicate_rows,
        "Missing Values": missing_values
    }

    st.json(report)

    st.markdown("---")

    # ==========================================================
    # Final Status
    # ==========================================================

    if duplicate_rows == 0 and missing_values == 0:

        st.success(
            "🎉 Dataset passed the basic quality checks."
        )

    else:

        st.warning(
            "⚠ Dataset still contains some quality issues."
        )