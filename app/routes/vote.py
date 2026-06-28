from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schema
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote_data: schema.Vote, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # 1. Verify if the target post actually exists before doing anything
    post_query = select(models.Post).where(models.Post.id == vote_data.post_id)
    post_exists = db.scalars(post_query).first()
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID {vote_data.post_id} does not exist"
        )

    # 2. Query to see if this specific user has already voted on this specific post
    vote_query = select(models.Vote).where(
        models.Vote.post_id == vote_data.post_id, 
        models.Vote.user_id == current_user.id
    )
    found_vote = db.scalars(vote_query).first()

    # Logic: If dir is 1, we are trying to add a vote
    if vote_data.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} has already voted on post {vote_data.post_id}"
            )
        
        # Create and add the new vote block record
        new_vote = models.Vote(post_id=vote_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vote does not exist"
            )
        
        db.delete(found_vote)
        db.commit()
        return {"message": "Successfully deleted vote"}