import streamlit as st
import os

from modules.report import generate_pdf_report


def show_report_page(df, cleaning_summary, ai_report=None, forecast_metrics=None):
    """
    Display the PDF Report Generation Page.
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
                📄 Business Analytics Report
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Generate a professional PDF report containing dataset summary, EDA, AI insights, and forecasting results."
    )

    st.markdown("---")

    st.success(
        "The report includes:\n"
        "- Dataset Overview\n"
        "- Data Cleaning Summary\n"
        "- EDA Summary\n"
        "- AI Business Insights\n"
        "- Forecasting Results\n"
        "- Final Conclusion"
    )

    st.markdown("---")

    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Generating PDF Report..."):

            try:

                pdf_path = generate_pdf_report(
                    df=df,
                    cleaning_summary=cleaning_summary,
                    ai_report=ai_report,
                    forecast_metrics=forecast_metrics
                )

                st.success("✅ PDF Generated Successfully!")

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(
                        label="⬇ Download Report",
                        data=pdf_file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(f"Error: {str(e)}")

    st.markdown("---")

    st.info(
        "💡 Tip: Generate AI Insights and Forecasting before creating the PDF for the most complete report."
    )