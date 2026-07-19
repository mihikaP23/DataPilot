import pandas as pd


def generate_summary(df):
    """
    Generate basic dataset summary.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Numeric Columns": len(df.select_dtypes(include="number").columns),
        "Categorical Columns": len(df.select_dtypes(include="object").columns),
        "Datetime Columns": len(df.select_dtypes(include="datetime").columns),
        "Memory Usage (MB)": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
    }

    return summary


def statistical_summary(df):
    """
    Returns descriptive statistics.
    """

    return df.describe(include="all").transpose()


def missing_values_report(df):
    """
    Returns missing value report.
    """

    missing = pd.DataFrame({
        "Missing Values": df.isnull().sum(),
        "Percentage (%)": round(df.isnull().mean() * 100, 2)
    })

    return missing[missing["Missing Values"] > 0]


def correlation_matrix(df):
    """
    Returns correlation matrix of numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    return numeric_df.corr()