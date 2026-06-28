from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as user_router
from routes.upload import router as upload_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "AI Business Intelligence Backend Running"
    }