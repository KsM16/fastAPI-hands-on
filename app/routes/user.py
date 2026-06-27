from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schema import UserCreate
from app.utils import hash_password
from app.database import get_db
from app import models

# 1. Initialize the router with prefix tags for grouping documentation
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Note: The route is now just "/", which combines with prefix to make "/users"
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    user.password = hash_password(user.password)
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
