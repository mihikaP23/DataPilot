
import os
from datetime import datetime
from xml.sax.saxutils import escape

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
            f"DataPilot_Report_{timestamp}.pdf"
        )

        self.styles = getSampleStyleSheet()
        self.story = []

    # =====================================================
    # TITLE
    # =====================================================

    def add_title(self):

        title = Paragraph(
            "<b><font size=22>DataPilot</font></b>",
            self.styles["Title"]
        )

        subtitle = Paragraph(
            "<font size=14>"
            "A Generative AI-Powered Business Intelligence Assistant"
            "</font>",
            self.styles["Heading2"]
        )

        report_name = Paragraph(
            "<b>Business Analytics Report</b>",
            self.styles["Heading1"]
        )

        date = Paragraph(
            f"Generated On: "
            f"{datetime.now().strftime('%d %B %Y %I:%M %p')}",
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
                f"<b>{escape(str(heading))}</b>",
                self.styles["Heading2"]
            )
        )

        self.story.append(Spacer(1, 0.15 * inch))

    # =====================================================
    # TABLE
    # =====================================================

    def add_table(self, data):

        table = Table(data, repeatRows=1)

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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
            ["Rows", str(df.shape[0])],
            ["Columns", str(df.shape[1])],
            ["Missing Values", str(int(df.isnull().sum().sum()))],
            ["Duplicate Rows", str(int(df.duplicated().sum()))],
            [
                "Numeric Columns",
                str(len(df.select_dtypes(include="number").columns))
            ],
            [
                "Categorical Columns",
                str(len(
                    df.select_dtypes(
                        include=["object", "category", "string"]
                    ).columns
                ))
            ]
        ]

        self.add_table(data)

    # =====================================================
    # CLEANING SUMMARY
    # =====================================================

    def add_cleaning_summary(self, summary):

        self.add_heading("2. Data Cleaning Summary")

        # Use safe defaults in case a summary field is unavailable.
        data = [
            ["Metric", "Value"],
            ["Original Rows", str(summary.get("original_rows", "N/A"))],
            ["Original Columns", str(summary.get("original_columns", "N/A"))],
            ["Missing Before", str(summary.get("missing_before", "N/A"))],
            ["Missing After", str(summary.get("missing_after", "N/A"))],
            ["Duplicates Removed", str(summary.get("duplicates_removed", "N/A"))]
        ]

        self.add_table(data)

    # =====================================================
    # EDA SUMMARY
    # =====================================================

    def add_eda_summary(self, df):

        self.add_heading("3. Dataset Analysis Summary")

        numeric = len(
            df.select_dtypes(include="number").columns
        )

        categorical = len(
            df.select_dtypes(
                include=["object", "category", "string"]
            ).columns
        )

        memory = round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2
        )

        data = [
            ["Metric", "Value"],
            ["Numeric Columns", str(numeric)],
            ["Categorical Columns", str(categorical)],
            ["Memory Usage (MB)", str(memory)]
        ]

        self.add_table(data)

    # =====================================================
    # AI INSIGHTS
    # =====================================================

    def add_ai_insights(self, ai_report):

        self.add_heading("4. AI Business Insights")

        if not ai_report or not str(ai_report).strip():
            ai_report = (
                "AI insights have not been generated yet. "
                "Please generate AI insights in the AI Insights "
                "section before creating the report."
            )

        # Escape special XML characters before passing text to ReportLab.
        safe_report = escape(str(ai_report))
        safe_report = safe_report.replace("\n", "<br/>")

        paragraph = Paragraph(
            safe_report,
            self.styles["BodyText"]
        )

        self.story.append(paragraph)
        self.story.append(Spacer(1, 0.30 * inch))

    # =====================================================
    # CONCLUSION
    # =====================================================

    def add_conclusion(self):

        self.add_heading("5. Final Conclusion")

        conclusion = (
            "DataPilot processes the uploaded dataset and provides "
            "dataset summaries and AI-powered business insights. "
            "Its natural-language question-answering functionality "
            "helps users explore their data and understand relevant "
            "patterns more easily. The generated report brings "
            "together dataset information, cleaning details, and "
            "AI-generated insights to support informed decisions."
        )

        self.story.append(
            Paragraph(
                escape(conclusion),
                self.styles["BodyText"]
            )
        )

    # =====================================================
    # SAVE PDF
    # =====================================================

    def save(self):

        doc = SimpleDocTemplate(
            self.filename,
            rightMargin=0.65 * inch,
            leftMargin=0.65 * inch,
            topMargin=0.65 * inch,
            bottomMargin=0.65 * inch
        )

        doc.build(self.story)

        return self.filename


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def generate_pdf_report(
    df,
    cleaning_summary,
    ai_report=None
):

    report = PDFReport()

    report.add_title()
    report.add_dataset_overview(df)
    report.add_cleaning_summary(cleaning_summary)
    report.add_eda_summary(df)
    report.add_ai_insights(ai_report)
    report.add_conclusion()

    return report.save()
