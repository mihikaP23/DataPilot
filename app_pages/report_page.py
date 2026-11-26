
import os
import streamlit as st

from modules.report import generate_pdf_report


def show_report_page(
    df,
    cleaning_summary,
    ai_report=None
):

    # Retrieve the AI report saved by the AI Insights page.
    if ai_report is None:
        ai_report = st.session_state.get("ai_report")

    st.markdown(
        """
        <h1 style="color:#1E3A8A;">📄 Business Analytics Report</h1>
        <p style="color:gray;">
            Generate a downloadable PDF containing your dataset overview,
            cleaning summary, analysis, and AI-generated business insights.
        </p>
        <hr>
        """,
        unsafe_allow_html=True
    )

    if ai_report:
        st.success("AI insights are available for the report.")
    else:
        st.info(
            "Generate AI insights in the AI Insights section first "
            "to include them in your PDF."
        )

    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True
    ):

        with st.spinner("Generating your PDF report..."):

            try:
                # Read the latest saved report when available.
                ai_report = st.session_state.get(
                    "ai_report",
                    ai_report
                )

                pdf_path = generate_pdf_report(
                    df=df,
                    cleaning_summary=cleaning_summary,
                    ai_report=ai_report
                )

                if not os.path.exists(pdf_path):
                    raise FileNotFoundError(
                        "The PDF report was not created."
                    )

                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()

                st.session_state["generated_pdf"] = pdf_bytes
                st.session_state["generated_pdf_name"] = (
                    os.path.basename(pdf_path)
                )

                st.success("PDF report generated successfully!")

            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    # Keep the download button available after the rerun.
    if st.session_state.get("generated_pdf"):
        st.download_button(
            label="⬇️ Download PDF Report",
            data=st.session_state["generated_pdf"],
            file_name=st.session_state.get(
                "generated_pdf_name",
                "DataPilot_Report.pdf"
            ),
            mime="application/pdf",
            use_container_width=True
        )

    st.caption(
        "Tip: Generate AI insights before creating the report "
        "to include them in the PDF."
    )
