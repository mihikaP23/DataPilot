
import streamlit as st
import pandas as pd

from modules.ai_insights import (
    generate_ai_report,
    answer_data_question,
)


def show_ai_page(df):
    """Display AI business insights and natural-language data Q&A."""

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
                🤖 DataPilot AI Business Insights
            </h2>
            <p style="margin-bottom:0;">
                Explore your business data using Generative AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df is None or df.empty:
        st.warning("Please upload a non-empty dataset first.")
        return

    st.write(
        "Generate AI-powered business insights or ask questions "
        "about your uploaded dataset using Llama 3.3 70B via Groq."
    )

    # Reset the conversation when the dataset changes.
    dataset_signature = (
        df.shape,
        tuple(map(str, df.columns)),
        df.head(3).to_json(
            orient="split",
            default_handler=str,
        ),
    )

    if st.session_state.get("ai_dataset_signature") != dataset_signature:
        st.session_state["ai_dataset_signature"] = dataset_signature
        st.session_state["ai_chat_history"] = []
        st.session_state["ai_report"] = None

    st.markdown("---")

    # =====================================================
    # SECTION 1: GENERATE BUSINESS INSIGHTS
    # =====================================================

    st.subheader("📊 AI Business Insights")

    st.write(
        "Generate an executive summary, key findings, risks, "
        "recommendations, and an overall assessment."
    )

    if st.button(
        "🚀 Generate AI Insights",
        use_container_width=True,
        type="primary",
        key="generate_ai_insights",
    ):
        with st.spinner("Analyzing the dataset using AI..."):
            report = generate_ai_report(df)

        st.session_state["ai_report"] = report

    report = st.session_state.get("ai_report")

    if report:
        st.markdown("---")
        st.markdown(report)

        st.download_button(
            label="📥 Download AI Report",
            data=report,
            file_name="DataPilot_AI_Business_Insights.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_ai_report",
        )

    st.markdown("---")

    # =====================================================
    # SECTION 2: ASK QUESTIONS ABOUT YOUR DATA
    # =====================================================

    st.subheader("💬 Chat with Your Data")

    st.write(
        "Ask questions in natural language. DataPilot uses "
        "available dataset statistics and calculated results "
        "to generate evidence-grounded answers."
    )

    with st.expander("Try example questions"):
        st.markdown(
            """
            - Which product or category has the highest total value?
            - Compare the highest-performing categories.
            - What are the strongest correlations in the data?
            - Summarize the important findings.
            - What additional information is needed to answer
              a question about this dataset?
            """
        )

    # Display previous messages.
    for message in st.session_state["ai_chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your dataset...",
        key="ai_data_question",
    )

    if question:
        # Show and save the user's question.
        st.session_state["ai_chat_history"].append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Generate the AI response.
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                answer = answer_data_question(df, question)

            st.markdown(answer)

        st.session_state["ai_chat_history"].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    if st.session_state["ai_chat_history"]:
        if st.button(
            "🗑️ Clear Chat",
            key="clear_ai_chat",
        ):
            st.session_state["ai_chat_history"] = []
            st.rerun()
