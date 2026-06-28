import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app import models
from app.config import settings  

# Use settings for token configuration 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token for a user."""
    to_encode = data.copy()
    
    # 2. Swap hardcoded expiration minutes with settings 
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    
    # 3. Swap hardcoded secret and algorithm with settings 
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """FastAPI Dependency: Intercepts requests, validates JWT token, and returns the User object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 4. Swap verification configs with settings [cite: 23]
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    statement = select(models.User).where(models.User.id == int(user_id))
    user = db.scalars(statement).first()
    
    if user is None:
        raise credentials_exception
        
    return user