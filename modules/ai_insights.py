import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AIInsights:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        self.client = Groq(api_key=api_key)

        self.model = "llama-3.3-70b-versatile"

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def generate_dataset_summary(self, df):

        summary = {}

        summary["rows"] = df.shape[0]
        summary["columns"] = df.shape[1]

        summary["column_names"] = list(df.columns)

        summary["numeric_columns"] = list(
            df.select_dtypes(include="number").columns
        )

        summary["categorical_columns"] = list(
            df.select_dtypes(include=["object", "category"]).columns
        )

        summary["missing_values"] = int(
            df.isnull().sum().sum()
        )

        summary["duplicate_rows"] = int(
            df.duplicated().sum()
        )

        summary["statistics"] = (
            df.describe(include="all")
            .fillna("")
            .to_string()
        )

        numeric_df = df.select_dtypes(include="number")

        if len(numeric_df.columns) >= 2:

            corr = numeric_df.corr()

            summary["correlation"] = corr.round(2).to_string()

        else:

            summary["correlation"] = "Not enough numeric columns."

        return summary

    # =====================================================
    # PROMPT CREATION
    # =====================================================

    def build_prompt(self, summary):

        prompt = f"""
You are a Senior Business Data Analyst.

Analyze the following dataset summary and generate
professional business insights.

Dataset Information

Rows : {summary['rows']}

Columns : {summary['columns']}

Column Names

{summary['column_names']}

Numeric Columns

{summary['numeric_columns']}

Categorical Columns

{summary['categorical_columns']}

Missing Values

{summary['missing_values']}

Duplicate Rows

{summary['duplicate_rows']}

Statistics

{summary['statistics']}

Correlation Matrix

{summary['correlation']}

Generate the report in EXACTLY this format.

# Executive Summary

(4-5 lines)

# Key Insights

- Bullet Points

# Risks

- Bullet Points

# Recommendations

- Bullet Points

# Overall Assessment

(3-4 lines)

Keep the language simple and business-oriented.
"""

        return prompt

    # =====================================================
    # GROQ API CALL
    # =====================================================

    def get_ai_insights(self, df):

        try:

            summary = self.generate_dataset_summary(df)

            prompt = self.build_prompt(summary)

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are an expert Business Analyst."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2,

                max_tokens=1500

            )

            answer = response.choices[0].message.content

            return answer

        except Exception as e:

            return f"Error : {str(e)}"


# =====================================================
# HELPER FUNCTION
# =====================================================

def generate_ai_report(df):

    ai = AIInsights()

    return ai.get_ai_insights(df)