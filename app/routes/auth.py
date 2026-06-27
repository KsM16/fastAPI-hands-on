from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models
from app.database import get_db
from app.schema import UserLogin
from app.utils import verify_password  

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", status_code=status.HTTP_200_OK)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    
    statement = select(models.User).where(models.User.email == user_credentials.email)
    user = db.scalars(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    return {"message": "Login successful!"}
