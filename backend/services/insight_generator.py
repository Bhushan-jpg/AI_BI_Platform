import pandas as pd


def generate_insights(df, analysis):

    insights = []

    # Dataset Overview
    insights.append(
        f"Dataset contains {analysis['rows']} rows and {analysis['columns']} columns."
    )

    insights.append(
        f"There are {analysis['duplicates']} duplicate records."
    )

    insights.append(
        f"There are {analysis['missing_values']} missing values."
    )

    # Column Insights
    for col in analysis["column_info"]:

        if col["type"] == "numeric":

            insights.append(
                f"'{col['name']}' is a numeric column with {col['unique_values']} unique values."
            )

        elif col["type"] == "categorical":

            insights.append(
                f"'{col['name']}' has {col['unique_values']} unique categories."
            )

        elif col["type"] == "datetime":

            insights.append(
                f"'{col['name']}' is identified as a date column."
            )

    # Missing Data
    missing_cols = []

    for c in df.columns:

        if df[c].isnull().sum() > 0:

            missing_cols.append(c)

    if missing_cols:

        insights.append(
            "Columns containing missing values: "
            + ", ".join(missing_cols)
        )

    # Numeric Statistics
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        insights.append(

            f"{col}: "

            f"Min={df[col].min()}, "

            f"Max={df[col].max()}, "

            f"Mean={round(df[col].mean(),2)}"

        )

    return insights