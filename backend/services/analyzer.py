import pandas as pd


def analyze_dataset(df):

    analysis = {}

    # Basic Information
    analysis["rows"] = int(df.shape[0])
    analysis["columns"] = int(df.shape[1])

    # Column Names
    analysis["column_names"] = df.columns.tolist()

    # Preview (First 10 Rows)
    analysis["preview"] = (
        df.head(10)
        .fillna("")
        .to_dict(orient="records")
    )

    # Data Quality
    analysis["duplicates"] = int(df.duplicated().sum())

    analysis["null_values"] = int(
        df.isnull().sum().sum()
    )

    # Column Counts
    numeric_cols = df.select_dtypes(include=["number"]).columns

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    analysis["numeric_columns"] = len(numeric_cols)

    analysis["categorical_columns"] = len(categorical_cols)

    # Detailed Column Information
    analysis["column_info"] = []

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):
            col_type = "numeric"

        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            col_type = "datetime"

        elif pd.api.types.is_bool_dtype(df[column]):
            col_type = "boolean"

        else:
            col_type = "categorical"

        analysis["column_info"].append({

            "name": column,

            "type": col_type,

            "unique_values": int(df[column].nunique()),

            "missing": int(df[column].isnull().sum())

        })

    return analysis