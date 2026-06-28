import pandas as pd


def generate_insights(df):

    insights = []

    # Dataset Overview
    insights.append(
        f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
    )

    # Missing Values
    missing = int(df.isnull().sum().sum())

    if missing == 0:
        insights.append(
            "No missing values found in the dataset."
        )
    else:
        insights.append(
            f"Dataset contains {missing} missing values."
        )

    # Duplicate Rows
    duplicates = int(df.duplicated().sum())

    if duplicates == 0:
        insights.append(
            "No duplicate records found."
        )
    else:
        insights.append(
            f"{duplicates} duplicate rows detected."
        )

    # Numeric Summary
    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) > 0:

        for col in numeric_cols:

            insights.append(
                f"{col}: Average = {round(df[col].mean(),2)}"
            )

    # Recommendation
    insights.append(
        "Review missing values and focus on the highest-performing metrics for better business decisions."
    )

    return insights