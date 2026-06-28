import pandas as pd


def analyze_dataset(df):

    analysis = {}

    analysis["rows"] = int(df.shape[0])
    analysis["columns"] = int(df.shape[1])

    analysis["duplicates"] = int(df.duplicated().sum())

    analysis["missing_values"] = int(
        df.isnull().sum().sum()
    )

    analysis["column_info"] = []

    for column in df.columns:

        dtype = str(df[column].dtype)

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