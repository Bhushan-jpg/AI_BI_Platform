from fastapi import FastAPI
from routes.users import router as user_router

from fastapi import Header
from auth import verify_token

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "AI Business Intelligence Backend Running"}

@app.get("/dashboard")
def dashboard():
    return {
        "message": "Welcome to AI BI Platform Dashboard"
    }

@app.get("/dashboard")
def dashboard(authorization: str = Header(None)):

    if authorization is None:
        return {
            "error": "Token Missing"
        }

    token = authorization.replace(
        "Bearer ",
        ""
    )

    user_email = verify_token(token)

    if not user_email:
        return {
            "error": "Invalid Token"
        }

    return {
        "message": f"Welcome {user_email}"
    }