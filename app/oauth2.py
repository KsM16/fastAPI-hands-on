import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "ddfrf334r34r3r3d4d34f4g45g54g54g45g45g45g45gg45g4g45g24234234234234234234234234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token for a user."""
    to_encode = data.copy()
    
    # Calculate token expiration timestamp safely in UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Sign and encode the JWT payload block
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """FastAPI Dependency: Intercepts requests, validates JWT token, and returns the User object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the signature using your local configurations
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    # Query database to extract the full verified User row properties
    statement = select(models.User).where(models.User.id == int(user_id))
    user = db.scalars(statement).first()
    
    if user is None:
        raise credentials_exception
        
    return user
