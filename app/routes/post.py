from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.schema import Post, PostUpdate
from app.database import get_db
from app import models

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
async def create_post(new_post: Post, db: Session = Depends(get_db)):
    db_post = models.Post(**new_post.model_dump())
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
async def delete_post(id: int, db: Session = Depends(get_db)):
    statement = delete(models.Post).where(models.Post.id == id)
    result = db.execute(statement)
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
    db.commit()
    return None


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db)):
    update_data = updated_post.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )

    statement = (
        update(models.Post)
        .where(models.Post.id == id)
        .values(**update_data)
        .returning(models.Post)
    )
    result = db.execute(statement)
    updated_record = result.scalar_one_or_none()
    
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
    db.commit()
    return updated_record
