from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password, create_access_token

from database import get_db
from models import User
from schemas import UserCreate
from auth import hash_password

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()

        return {"message": "User Registered Successfully"}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(
        user.password,
        db_user.password
    ):
        return {"error": "Invalid password"}

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }