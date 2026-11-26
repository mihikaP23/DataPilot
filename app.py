
import os
import streamlit as st

# ==========================
# Import Modules
# ==========================
from modules.upload import upload_dataset
from modules.cleaning import clean_data

# ==========================
# Import Pages
# ==========================
from app_pages.overview import show_overview
from app_pages.eda_page import show_eda
from app_pages.ai_page import show_ai_page
from app_pages.report_page import show_report_page


# ==========================
# Load Custom CSS
# ==========================
def load_css():
    css_path = os.path.join("assets", "style.css")

    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="DataPilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# ==========================
# Header
# ==========================
st.markdown(
    """
    <h1 style='text-align:center;color:#1E3A8A;'>
        📊 DataPilot
    </h1>

    <h4 style='text-align:center;color:gray;'>
        A Generative AI-Powered Business Intelligence Assistant
    </h4>

    <p style='text-align:center;color:#6B7280;font-size:17px;'>
        Upload • Analyze • Ask AI • Generate Reports
    </p>

    <hr>
    """,
    unsafe_allow_html=True
)


# ==========================
# Sidebar
# ==========================
st.sidebar.markdown(
    """
# 📊 DataPilot

### GenAI-Powered Data Analysis

---
"""
)




# ==========================
# Upload Dataset
# ==========================
df = upload_dataset()


# ==========================
# Main Application
# ==========================
if df is not None:

    st.success("✅ Dataset uploaded successfully!")

    cleaned_df, cleaning_summary = clean_data(df)

    page = st.sidebar.radio(
        "📂 Navigation",
        [
            "📊 Overview",
            "📈 EDA",
            "🤖 AI Insights & Q&A",
            "📄 Report"
        ]
    )

    # ======================
    # Overview
    # ======================
    if page == "📊 Overview":
        show_overview(
            original_df=df,
            cleaned_df=cleaned_df,
            summary=cleaning_summary
        )

    # ======================
    # EDA
    # ======================
    elif page == "📈 EDA":
        show_eda(cleaned_df)

    # ======================
    # AI Insights & Q&A
    # ======================
    elif page == "🤖 AI Insights & Q&A":
        show_ai_page(cleaned_df)

    # ======================
    # Report
    # ======================
    elif page == "📄 Report":

        show_report_page(
            cleaned_df,
            cleaning_summary,
            ai_report=st.session_state.get("ai_report")
        )

else:

    st.info("📁 Upload a CSV or Excel dataset to begin your analysis.")

    st.markdown(
        """
### 🚀 Features

- 📂 Upload CSV / Excel Files
- 🧹 Automatic Data Cleaning
- 📊 Dataset Summaries and Exploratory Analysis
- 🤖 AI-Generated Business Insights
- 💬 Natural-Language Questions About Your Data
- 📄 Downloadable PDF Reports

---
"""
    )
