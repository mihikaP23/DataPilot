import streamlit as st

from modules.ai_insights import generate_ai_report


def show_ai_page(df):
    """
    Displays the AI Business Insights page.
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
                🤖 AI Business Insights
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Generate AI-powered business insights from your cleaned dataset using Groq Llama 3.3 70B."
    )

    st.markdown("---")

    st.info(
        "The AI analyzes the dataset summary instead of the complete dataset to reduce token usage and improve performance."
    )

    st.markdown("")

    if st.button(
        "🚀 Generate AI Insights",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Analyzing dataset using AI..."):

            report = generate_ai_report(df)

        st.success("Analysis Complete!")

        st.markdown("---")

        st.markdown(report)

        st.markdown("---")

        st.download_button(

            label="📥 Download AI Report",

            data=report,

            file_name="AI_Business_Insights.txt",

            mime="text/plain",

            use_container_width=True

        )