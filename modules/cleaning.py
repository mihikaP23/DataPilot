
import pandas as pd


def clean_data(df):
    """
    Cleans the uploaded dataset.

    Steps:
        1. Count original duplicate rows.
        2. Remove original duplicates.
        3. Handle numeric missing values using median.
        4. Handle categorical missing values using mode.
        5. Verify the final dataset.

    Returns:
        cleaned_df, summary
    """

    # Validate input
    if df is None:
        raise ValueError("No dataset provided.")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")

    if df.empty:
        raise ValueError("The uploaded dataset is empty.")

    cleaned_df = df.copy()

    # =====================================================
    # STEP 1: ORIGINAL DATASET SUMMARY
    # =====================================================

    original_rows = len(cleaned_df)

    original_duplicates = int(
        cleaned_df.duplicated().sum()
    )

    summary = {
        "original_rows": int(original_rows),
        "original_columns": int(len(cleaned_df.columns)),
        "missing_before": int(
            cleaned_df.isnull().sum().sum()
        ),
        "original_duplicates": original_duplicates,
        "duplicates_removed": original_duplicates,
        "missing_after": 0
    }

    # =====================================================
    # STEP 2: REMOVE ORIGINAL DUPLICATES
    # =====================================================

    cleaned_df = cleaned_df.drop_duplicates(
        keep="first"
    ).copy()

    # =====================================================
    # STEP 3: DETECT COLUMN TYPES
    # =====================================================

    numeric_columns = cleaned_df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    # =====================================================
    # STEP 4: HANDLE NUMERIC MISSING VALUES
    # =====================================================

    for column in numeric_columns:

        if cleaned_df[column].isnull().any():

            median_value = cleaned_df[column].median()

            if pd.notna(median_value):
                cleaned_df[column] = cleaned_df[column].fillna(
                    median_value
                )

    # =====================================================
    # STEP 5: HANDLE CATEGORICAL MISSING VALUES
    # =====================================================

    for column in categorical_columns:

        if cleaned_df[column].isnull().any():

            mode_values = cleaned_df[column].mode(
                dropna=True
            )

            if not mode_values.empty:

                cleaned_df[column] = cleaned_df[column].fillna(
                    mode_values.iloc[0]
                )

            else:

                cleaned_df[column] = cleaned_df[column].fillna(
                    "Unknown"
                )

    # =====================================================
    # STEP 6: FINAL VERIFICATION
    # =====================================================

    cleaned_df = cleaned_df.reset_index(drop=True)

    summary["missing_after"] = int(
        cleaned_df.isnull().sum().sum()
    )

    summary["cleaned_rows"] = int(len(cleaned_df))

    summary["remaining_duplicates"] = int(
        cleaned_df.duplicated().sum()
    )

    # =====================================================
    # PRINT CLEANING SUMMARY
    # =====================================================

    print("\n========== DATA CLEANING SUMMARY ==========")

    print("Original Rows:", summary["original_rows"])
    print("Cleaned Rows:", summary["cleaned_rows"])
    print("Original Columns:", summary["original_columns"])

    print("Missing Values Before:", summary["missing_before"])
    print("Missing Values After:", summary["missing_after"])

    print("Original Duplicate Rows:",
          summary["original_duplicates"])

    print("Duplicates Removed:",
          summary["duplicates_removed"])

    print("Remaining Duplicates:",
          summary["remaining_duplicates"])

    print("===========================================\n")

    return cleaned_df, summary
