import pandas as pd


def clean_data(df):
    """
    Cleans the uploaded dataset.

    Parameters:
        df (pd.DataFrame)

    Returns:
        cleaned_df (pd.DataFrame)
        summary (dict)
    """

    cleaned_df = df.copy()

    summary = {
        "original_rows": len(df),
        "original_columns": len(df.columns),
        "missing_before": int(df.isnull().sum().sum()),
        "duplicates_removed": 0,
        "missing_after": 0
    }

    # Remove duplicate rows
    duplicate_count = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates()

    summary["duplicates_removed"] = int(duplicate_count)

    # Detect column types
    numeric_columns = cleaned_df.select_dtypes(include="number").columns
    categorical_columns = cleaned_df.select_dtypes(include="object").columns

    # Fill numeric missing values with median
    for column in numeric_columns:
        if cleaned_df[column].isnull().sum() > 0:
            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].median()
            )

    # Fill categorical missing values with mode
    for column in categorical_columns:
        if cleaned_df[column].isnull().sum() > 0:

            mode = cleaned_df[column].mode()

            if not mode.empty:
                cleaned_df[column] = cleaned_df[column].fillna(mode[0])
            else:
                cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    summary["missing_after"] = int(cleaned_df.isnull().sum().sum())

    return cleaned_df, summary