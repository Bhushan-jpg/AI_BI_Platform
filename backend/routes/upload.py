from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io


router = APIRouter()



def generate_ai_charts(df):

    charts = []

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns


    text_cols = df.select_dtypes(
        include=["object"]
    ).columns



    if len(text_cols) > 0 and len(numeric_cols) > 0:


        valid_text_cols = [
            col for col in text_cols
            if "id" not in col.lower()
        ]


        if len(valid_text_cols) == 0:
            return charts


        category_col = valid_text_cols[0]


        preferred_numbers = [
            col for col in numeric_cols
            if any(
                word in col.lower()
                for word in [
                    "sales",
                    "price",
                    "cost",
                    "amount",
                    "revenue",
                    "income"
                ]
            )
        ]



        if preferred_numbers:
            value_col = preferred_numbers[0]

        else:
            value_col = numeric_cols[0]



        analysis = (
            df.groupby(category_col)[value_col]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )



        highest = analysis.iloc[0]



        charts.append({

            "title":
            f"{value_col} by {category_col}",


            "type":
            "bar",


            "data":
            analysis.to_dict(
                orient="records"
            ),


            "x":
            category_col,


            "y":
            value_col,


            "explanation":
            f"This chart explains {value_col} performance across {category_col}.",


            "insight":
            f"{highest[category_col]} is the highest performing group.",


            "recommendation":
            "Focus business decisions on high performing segments."

        })


    return charts





@router.post("/upload")
async def upload(file: UploadFile = File(...)):


    contents = await file.read()



    df = pd.read_excel(
        io.BytesIO(contents)
    )



    rows = df.shape[0]

    columns = df.shape[1]



    dynamic_charts = generate_ai_charts(df)



    return {


        # basic info
        "filename": file.filename,

        "rows": rows,

        "columns": columns,



        # columns
        "column_names":
        df.columns.tolist(),



        # table preview
        "preview":
        df.head(10)
        .to_dict(
            orient="records"
        ),



        # data quality cards
        "duplicates":
        int(
            df.duplicated().sum()
        ),



        "null_values":
        int(
            df.isnull().sum().sum()
        ),



        "numeric_columns":
        len(
            df.select_dtypes(
                include=["number"]
            ).columns
        ),



        "categorical_columns":
        len(
            df.select_dtypes(
                include=["object"]
            ).columns
        ),



        # AI charts
        "dynamic_charts":
        dynamic_charts,



        # insights
        "insights":[

            "Dataset analyzed successfully",

            f"{columns} columns detected",

            f"{rows} records processed"

        ]

    }