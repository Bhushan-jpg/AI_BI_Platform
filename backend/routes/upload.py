from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

from services.analyzer import analyze_dataset
from services.chart_generator import generate_ai_charts
from services.insight_generator import generate_insights

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    contents = await file.read()

    df = pd.read_excel(
        io.BytesIO(contents)
    )

    # Dataset Analysis
    analysis = analyze_dataset(df)

    # AI Charts
    charts = generate_ai_charts(df)

    # AI Insights
    insights = generate_insights(df)

    # Final Response
    return {

        "filename": file.filename,

        **analysis,

        "dynamic_charts": charts,

        "insights": insights

    }