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
from app_pages.dashboard_page import show_dashboard
from app_pages.ai_page import show_ai_page
from app_pages.forecast_page import show_forecasting
from app_pages.report_page import show_report_page


# ==========================
# Load Custom CSS
# ==========================
def load_css():
    css_path = os.path.join("assets", "style.css")

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="InsightForge",
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
        📊 InsightForge
    </h1>

    <h4 style='text-align:center;color:gray;'>
        AI-Powered Business Analytics Platform
    </h4>

    <p style='text-align:center;color:#6B7280;font-size:17px;'>
        Upload • Clean • Analyze • Visualize • Forecast • Generate AI Insights
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
# 📊 InsightForge

### AI-Powered Business Analytics

---
"""
)

st.sidebar.success("Version 1.0")

st.sidebar.caption(
    "Built with ❤️ using Python, Streamlit & AI"
)

st.sidebar.markdown("---")


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
            "📉 Dashboard",
            "🤖 AI Insights",
            "📈 Forecasting",
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
    # Dashboard
    # ======================
    elif page == "📉 Dashboard":

        show_dashboard(cleaned_df)

    # ======================
    # AI Insights
    # ======================
    elif page == "🤖 AI Insights":

        show_ai_page(cleaned_df)

    # ======================
    # Forecasting
    # ======================
    elif page == "📈 Forecasting":

        show_forecasting(cleaned_df)

    # ======================
    # Report
    # ======================
    elif page == "📄 Report":

        show_report_page(
            cleaned_df,
            cleaning_summary
        )

else:

    st.info("📁 Upload a CSV or Excel dataset to begin your analysis.")

    st.markdown(
        """
### 🚀 Features

- 📂 Upload CSV / Excel Files
- 🧹 Automatic Data Cleaning
- 📊 Exploratory Data Analysis (EDA)
- 📉 Interactive Dashboard
- 🤖 AI Business Insights
- 📈 Machine Learning Forecasting
- 📄 Professional PDF Report

---
"""
    )