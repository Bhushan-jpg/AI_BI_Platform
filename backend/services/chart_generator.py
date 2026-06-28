import pandas as pd


def generate_ai_charts(df):

    charts = []

    # Detect columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_cols = [
        col for col in df.select_dtypes(include=["object", "category"]).columns
        if "id" not in col.lower()
    ]

    if not numeric_cols or not categorical_cols:
        return charts

    # Choose best numeric column
    preferred = [
        "sales",
        "revenue",
        "profit",
        "amount",
        "price",
        "cost",
        "income",
        "quantity"
    ]

    value_col = None

    for keyword in preferred:
        for col in numeric_cols:
            if keyword in col.lower():
                value_col = col
                break
        if value_col:
            break

    if value_col is None:
        value_col = numeric_cols[0]

    # ---------- BAR CHART ----------
    category_col = categorical_cols[0]

    bar_data = (
        df.groupby(category_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    charts.append({

        "title": f"{value_col} by {category_col}",

        "type": "bar",

        "data": bar_data.fillna("").to_dict(orient="records"),

        "x": category_col,

        "y": value_col,

        "explanation":
        f"This chart compares {value_col} across {category_col}.",

        "insight":
        f"{bar_data.iloc[0][category_col]} has the highest {value_col}.",

        "recommendation":
        "Focus business efforts on the highest performing category."

    })

    # ---------- PIE CHART ----------
    pie_data = (
        df.groupby(category_col)[value_col]
        .sum()
        .head(6)
        .reset_index()
    )

    charts.append({

        "title": f"{value_col} Distribution",

        "type": "pie",

        "data": pie_data.fillna("").to_dict(orient="records"),

        "x": category_col,

        "y": value_col,

        "explanation":
        f"Distribution of {value_col}.",

        "insight":
        "Shows the contribution of each category.",

        "recommendation":
        "Maintain balance across categories."

    })

    # ---------- LINE CHART ----------
    datetime_cols = df.select_dtypes(
        include=["datetime64", "datetime64[ns]"]
    ).columns.tolist()

    if datetime_cols:

        date_col = datetime_cols[0]

        line_data = (
            df.groupby(date_col)[value_col]
            .sum()
            .reset_index()
        )

        charts.append({

            "title": f"{value_col} Trend",

            "type": "line",

            "data": line_data.fillna("").to_dict(orient="records"),

            "x": date_col,

            "y": value_col,

            "explanation":
            f"Trend of {value_col} over time.",

            "insight":
            "Shows performance changes over time.",

            "recommendation":
            "Monitor trends for forecasting."

        })

    return charts