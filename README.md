# DataPilot – A Generative AI-Powered Business Intelligence Assistant

DataPilot is a Generative AI-powered Business Intelligence assistant designed to simplify data analysis and help users extract meaningful insights from structured datasets. It combines automated data preprocessing, Exploratory Data Analysis (EDA), interactive dashboards, AI-generated business insights, forecasting, and report generation within an interactive application.

## Overview

Analyzing business data manually can be time-consuming, especially for users without technical expertise. DataPilot streamlines this process by allowing users to upload datasets, automatically process the data, explore visual patterns, and obtain AI-generated insights to support data-driven decision-making.

## Features

- **Data Upload:** Upload datasets for analysis.
- **Automated Data Cleaning:** Handle missing values, duplicate records, and data preprocessing.
- **Exploratory Data Analysis (EDA):** Explore statistical summaries, distributions, correlations, and trends.
- **Interactive Dashboards:** Generate visualizations and KPIs to understand business performance.
- **Generative AI Insights:** Generate data-driven insights, summaries, recommendations, and answers to analytical queries using an LLM.
- **Forecasting:** Perform predictive analysis using Machine Learning techniques.
- **Report Generation:** Generate analytical reports summarizing dataset characteristics, findings, and insights.

## System Workflow

1. Upload the dataset.
2. Perform automated data cleaning and preprocessing.
3. Explore the dataset through EDA.
4. Generate interactive dashboards and visualizations.
5. Obtain AI-powered insights and recommendations.
6. Perform forecasting where applicable.
7. Generate analytical reports.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive application interface |
| Pandas | Data processing and manipulation |
| NumPy | Numerical computations |
| Matplotlib / Plotly | Data visualization |
| Scikit-learn | Machine Learning and forecasting |
| Groq API | Generative AI-powered analysis |
| LLaMA 3.3 70B Versatile | Language model for AI insights |
| ReportLab | PDF report generation |

## Project Structure

```text
DataPilot/
│
├── app.py
├── app_pages/
│   ├── overview.py
│   ├── eda.py
│   ├── dashboard.py
│   ├── ai.py
│   ├── forecast.py
│   └── report.py
│
├── assets/
│   └── style.css
│
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mihikaP23/DataPilot.git
```

### 2. Navigate to the project directory

```bash
cd DataPilot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Groq API Key

Create a `.env` file in the root directory and add:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual API key.

### 7. Run the application

```bash
streamlit run app.py
```

## Generative AI Integration

DataPilot integrates the Groq API with the LLaMA 3.3 70B Versatile model to analyze dataset summaries and generate natural-language business insights.

The AI component helps users interpret analytical results, identify meaningful patterns, summarize observations, and obtain recommendations based on the provided dataset context.

## Machine Learning

DataPilot incorporates Machine Learning-based forecasting to explore predictive trends in data. Linear Regression is used for forecasting in the implemented model, with model performance evaluated using relevant regression metrics.

## Future Scope

- Integration of additional Machine Learning models.
- Enhanced natural-language querying capabilities.
- Advanced predictive analytics.
- Support for additional dataset formats and analytical workflows.
- Improved AI-driven business decision support.

## Author

**Mihika Pargai**

B.Tech – Computer Science Engineering (Data Science)

GitHub: [mihikaP23](https://github.com/mihikaP23)

---

*DataPilot – Turning data into meaningful insights.*
