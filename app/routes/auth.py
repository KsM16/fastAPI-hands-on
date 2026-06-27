from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models
from app.database import get_db
from app.schema import UserLogin, Token  # Import your Token schema
from app.utils import verify_password
from app.oauth2 import create_access_token  # Import your token generation utility

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    
    statement = select(models.User).where(models.User.email == user_credentials.email)
    user = db.scalars(statement).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
    # Create the token content package (we pass the user's primary key ID)
    access_token = create_access_token(data={"user_id": user.id})
    
    # Return token payload matching the structure of your schema
    return {"access_token": access_token, "token_type": "bearer"}
