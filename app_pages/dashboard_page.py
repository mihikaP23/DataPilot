import streamlit as st
import plotly.express as px

from modules.dashboard import (
    generate_kpis,
    get_numeric_columns,
    get_categorical_columns,
    create_bar_chart,
    create_line_chart,
    create_scatter_plot
)


def show_dashboard(df):

    st.markdown("""
        <div style="
            background:linear-gradient(90deg,#2563EB,#1E3A8A);
            padding:20px;
            border-radius:15px;
            color:white;
        ">
            <h2 style="color:white;">
                📊 Interactive Business Dashboard
            </h2>


        </div>
        """, 
        unsafe_allow_html=True
    )

    st.write(
        "Explore your data through interactive visualizations and KPIs"
    )

    st.markdown("---")

    # ==========================================================
    # KPIs
    # ==========================================================

    kpis = generate_kpis(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📄 Rows", f"{kpis['Rows']:,}")

    c2.metric("📊 Columns", kpis["Columns"])

    c3.metric("🔢 Numeric", kpis["Numeric Columns"])

    c4.metric("🔤 Categories", kpis["Categorical Columns"])

    c5.metric("❗ Missing", kpis["Missing Values"])

    st.markdown("---")

    # ==========================================================
    # Sidebar Filters
    # ==========================================================

    st.sidebar.subheader("📊 Dashboard Filters")

    numeric_columns = get_numeric_columns(df)

    categorical_columns = get_categorical_columns(df)

    all_columns = list(df.columns)

    x_column = st.sidebar.selectbox(
        "X Axis",
        all_columns
    )

    y_column = st.sidebar.selectbox(
        "Y Axis",
        numeric_columns
    )

    st.subheader("📈 Business Visualizations")

    # ==========================================================
    # FIRST ROW
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(

            create_bar_chart(
                df,
                x_column,
                y_column
            ),

            width="stretch"

        )

    with col2:

        st.plotly_chart(

            create_line_chart(
                df,
                x_column,
                y_column
            ),

            width="stretch"

        )

    # ==========================================================
    # SECOND ROW
    # ==========================================================

    col3, col4 = st.columns(2)

    with col3:

        st.plotly_chart(

            create_scatter_plot(
                df,
                x_column,
                y_column
            ),

            width="stretch"

        )

    with col4:

        if categorical_columns:

            pie_col = st.selectbox(
                "Pie Chart Category",
                categorical_columns
            )

            pie = px.pie(

                df,

                names=pie_col,

                title=f"{pie_col} Distribution"

            )

            st.plotly_chart(
                pie,
                width="stretch"
            )

        else:

            st.info("No categorical columns available.")

    st.markdown("---")

    # ==========================================================
    # HISTOGRAM
    # ==========================================================

    st.subheader("📊 Distribution")

    hist_column = st.selectbox(
        "Histogram Column",
        numeric_columns
    )

    histogram = px.histogram(

        df,

        x=hist_column,

        nbins=30,

        title=f"Distribution of {hist_column}"

    )

    st.plotly_chart(

        histogram,

        width="stretch"

    )

    st.markdown("---")

    # ==========================================================
    # CORRELATION HEATMAP
    # ==========================================================

    if len(numeric_columns) >= 2:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_columns].corr()

        heatmap = px.imshow(

            corr,

            text_auto=True,

            color_continuous_scale="Blues"

        )

        st.plotly_chart(

            heatmap,

            width="stretch"

        )

    st.markdown("---")

    # ==========================================================
    # DATA PREVIEW
    # ==========================================================

    st.subheader("📄 Dataset Preview")

    rows = st.slider(

        "Rows to Display",

        5,

        100,

        20

    )

    st.dataframe(

        df.head(rows),

        width="stretch",

        height=450

    )

    csv = df.to_csv(index=False)

    st.download_button(

        "📥 Download Dataset",

        csv,

        "cleaned_dataset.csv",

        "text/csv",

        width="stretch"

    )