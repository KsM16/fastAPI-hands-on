from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.schema import Post, PostUpdate
from app.database import get_db
from app import models

from app.oauth2 import get_current_user  




router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Post])
async def get_posts(db: Session = Depends(get_db)):
    statement = select(models.Post)
    posts = db.scalars(statement).all()
    return posts


@router.post("/trial", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    new_post: Post, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)   
):
    print(f"Post being created by user ID: {current_user.id}")
    
    # Unpack the schema data and explicitly assign the owner_id
    db_post = models.Post(**new_post.model_dump(), owner_id=current_user.id)
    
    db.add(db_post)     
    db.commit()          
    db.refresh(db_post)   
    return db_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    statement = select(models.Post).where(models.Post.id == id)
    result = db.scalars(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID {id} was not found"
        )
    return result 


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Add authentication dependency
):
    # First, fetch the post to check ownership
    statement = select(models.Post).where(models.Post.id == id)
    post = db.scalars(statement).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
        
    # Check if the logged-in user owns the post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    db.delete(post)
    db.commit()
    return None


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(
    id: int, 
    updated_post: PostUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Add authentication dependency
):
    update_data = updated_post.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )

    # First, fetch the post to check ownership
    select_statement = select(models.Post).where(models.Post.id == id)
    post = db.scalars(select_statement).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
        
    # Check if the logged-in user owns the post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    # Perform the update
    update_statement = (
        update(models.Post)
        .where(models.Post.id == id)
        .values(**update_data)
        .returning(models.Post)
    )
    result = db.execute(update_statement)
    updated_record = result.scalar_one_or_none()
    
    db.commit()
    return updated_record



