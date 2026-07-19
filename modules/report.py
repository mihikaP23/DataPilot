import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ==========================================================
# PDF REPORT CLASS
# ==========================================================

class PDFReport:

    def __init__(self):
        reports_folder = "reports"
        os.makedirs(reports_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(
            reports_folder,
            f"InsightForge_Report_{timestamp}.pdf"
        )
        self.styles = getSampleStyleSheet()
        self.story = []
    # =====================================================
    # TITLE
    # =====================================================

    def add_title(self):
        title = Paragraph(
            "<b><font size=22>InsightForge</font></b>",
            self.styles["Title"]
        )

        subtitle = Paragraph(
            "<font size=14>AI-Powered Business Analytics Platform</font>",
            self.styles["Heading2"]
        )

        report_name = Paragraph(
            "<b>Business Analytics Report</b>",
            self.styles["Heading1"]
        )

        date = Paragraph(
            f"Generated On : {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            self.styles["Normal"]
        )

        self.story.append(title)
        self.story.append(Spacer(1, 0.20 * inch))

        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.25 * inch))

        self.story.append(report_name)
        self.story.append(Spacer(1, 0.30 * inch))

        self.story.append(date)
        self.story.append(Spacer(1, 0.50 * inch))

    # =====================================================
    # SECTION HEADING
    # =====================================================

    def add_heading(self, heading):

        self.story.append(

            Paragraph(

                f"<b>{heading}</b>",

                self.styles["Heading2"]

            )

        )

        self.story.append(Spacer(1, 0.15 * inch))

    # =====================================================
    # TABLE
    # =====================================================

    def add_table(self, data):

        table = Table(data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, -1), "CENTER")

            ])

        )

        self.story.append(table)

        self.story.append(Spacer(1, 0.30 * inch))

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    def add_dataset_overview(self, df):

        self.add_heading("1. Dataset Overview")

        data = [

            ["Metric", "Value"],

            ["Rows", df.shape[0]],

            ["Columns", df.shape[1]],

            ["Missing Values", int(df.isnull().sum().sum())],

            ["Duplicate Rows", int(df.duplicated().sum())],

            [

                "Numeric Columns",

                len(df.select_dtypes(include="number").columns)

            ],

            [

                "Categorical Columns",

                len(

                    df.select_dtypes(

                        include=["object", "category"]

                    ).columns

                )

            ]

        ]

        self.add_table(data)

    # =====================================================
    # CLEANING SUMMARY
    # =====================================================

    def add_cleaning_summary(self, summary):

        self.add_heading("2. Data Cleaning Summary")

        data = [

            ["Metric", "Value"],

            ["Original Rows", summary["original_rows"]],

            ["Original Columns", summary["original_columns"]],

            ["Missing Before", summary["missing_before"]],

            ["Missing After", summary["missing_after"]],

            ["Duplicates Removed", summary["duplicates_removed"]]

        ]

        self.add_table(data)

    # =====================================================
    # EDA SUMMARY
    # =====================================================

    def add_eda_summary(self, df):

        self.add_heading("3. Exploratory Data Analysis")

        numeric = len(

            df.select_dtypes(include="number").columns

        )

        categorical = len(

            df.select_dtypes(

                include=["object", "category"]

            ).columns

        )

        memory = round(

            df.memory_usage(

                deep=True

            ).sum() / (1024 * 1024),

            2

        )

        data = [

            ["Metric", "Value"],

            ["Numeric Columns", numeric],

            ["Categorical Columns", categorical],

            ["Memory Usage (MB)", memory]

        ]

        self.add_table(data)

        # =====================================================
    # AI INSIGHTS
    # =====================================================

    def add_ai_insights(self, ai_report):

        self.add_heading("4. AI Business Insights")

        if not ai_report:

            ai_report = "AI insights were not generated."

        paragraph = Paragraph(

            ai_report.replace("\n", "<br/>"),

            self.styles["BodyText"]

        )

        self.story.append(paragraph)

        self.story.append(Spacer(1, 0.30 * inch))

    # =====================================================
    # FORECASTING RESULTS
    # =====================================================

    def add_forecasting_results(self, metrics):

        self.add_heading("5. Forecasting Results")

        if metrics is None:

            data = [

                ["Metric", "Value"],

                ["Status", "Forecasting not executed"]

            ]

        else:

            data = [

                ["Metric", "Value"],

                ["Model", "Linear Regression"],

                ["R² Score", metrics["R2 Score"]],

                ["MAE", metrics["MAE"]],

                ["MSE", metrics["MSE"]],

                ["RMSE", metrics["RMSE"]]

            ]

        self.add_table(data)

    # =====================================================
    # CONCLUSION
    # =====================================================

    def add_conclusion(self):

        self.add_heading("6. Final Conclusion")

        conclusion = """
InsightForge successfully analyzed the uploaded dataset
through automated data cleaning, exploratory data analysis,
interactive visualization, AI-powered business insights,
and machine learning forecasting.

The generated insights can assist organizations in making
data-driven business decisions while reducing manual effort.
"""

        self.story.append(

            Paragraph(

                conclusion,

                self.styles["BodyText"]

            )

        )

    # =====================================================
    # SAVE PDF
    # =====================================================

    def save(self):

        doc = SimpleDocTemplate(

            self.filename

        )

        doc.build(

            self.story

        )

        return self.filename


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def generate_pdf_report(

    df,

    cleaning_summary,

    ai_report=None,

    forecast_metrics=None

):

    report = PDFReport()

    report.add_title()

    report.add_dataset_overview(df)

    report.add_cleaning_summary(cleaning_summary)

    report.add_eda_summary(df)

    report.add_ai_insights(ai_report)

    report.add_forecasting_results(

        forecast_metrics

    )

    report.add_conclusion()

    file_path = report.save()

    return file_path