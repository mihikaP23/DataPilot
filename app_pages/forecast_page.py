import streamlit as st
import plotly.express as px

from modules.forecasting import (
    get_numeric_columns,
    train_model
)


def show_forecasting(df):
    """
    Displays the Forecasting page.
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
                📈 Sales & Trend Forecasting
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Train a Machine Learning model to predict any numeric column."
    )

    st.markdown("---")

    # =====================================================
    # NUMERIC COLUMNS
    # =====================================================

    numeric_columns = get_numeric_columns(df)

    if len(numeric_columns) < 2:

        st.warning(
            "At least two numeric columns are required for forecasting."
        )

        return

    # =====================================================
    # TARGET COLUMN
    # =====================================================

    target_column = st.selectbox(

        "🎯 Select Target Column",

        numeric_columns

    )

    st.info(
        f"Selected Target : **{target_column}**"
    )

    st.markdown("---")

    # =====================================================
    # TRAIN MODEL
    # =====================================================

    if st.button(
        "🚀 Train Forecasting Model",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Training Linear Regression Model..."):

            try:

                model, prediction_df, metrics = train_model(
                    df,
                    target_column
                )

            except Exception as e:

                st.error(str(e))

                return

        st.success("✅ Model Trained Successfully!")

        st.markdown("---")

        # =====================================================
        # METRICS
        # =====================================================

        st.subheader("📊 Model Performance")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "R² Score",
            metrics["R2 Score"]
        )

        col2.metric(
            "MAE",
            metrics["MAE"]
        )

        col3.metric(
            "MSE",
            metrics["MSE"]
        )

        col4.metric(
            "RMSE",
            metrics["RMSE"]
        )

        st.markdown("---")

        # =====================================================
        # ACTUAL VS PREDICTED
        # =====================================================

        st.subheader("📈 Actual vs Predicted")

        fig = px.line(

            prediction_df,

            y=[
                "Actual",
                "Predicted"
            ],

            title="Actual vs Predicted Values",

            markers=True

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        # =====================================================
        # SCATTER PLOT
        # =====================================================

        st.subheader("🎯 Prediction Accuracy")

        scatter = px.scatter(

            prediction_df,

            x="Actual",

            y="Predicted",

            title="Actual vs Predicted Scatter"

        )

        st.plotly_chart(

            scatter,

            use_container_width=True

        )

        st.markdown("---")

        # =====================================================
        # PREDICTION TABLE
        # =====================================================

        st.subheader("📄 Prediction Results")

        st.dataframe(

            prediction_df,

            use_container_width=True,

            height=400

        )

        csv = prediction_df.to_csv(index=False)

        st.download_button(

            "📥 Download Predictions",

            csv,

            "predictions.csv",

            "text/csv",

            use_container_width=True

        )