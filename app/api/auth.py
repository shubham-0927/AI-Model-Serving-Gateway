from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import register_user, login_user
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password)
    return {"message": "User created", "user_id": user.id}

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, data.email, data.password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"access_token": token}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "email": current_user.email
    }