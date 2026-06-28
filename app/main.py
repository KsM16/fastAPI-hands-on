from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import post, user, auth, vote  

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],          
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)  

@app.get("/")
async def root():
    return {"message": "HelloJII World"}






# import bcrypt
# from fastapi import Body, Depends, FastAPI, HTTPException, status
# from pydantic import BaseModel
# from typing import Optional
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# from sqlalchemy import delete, select, update
# from sqlalchemy.orm import Session

# # Explicitly import BOTH validation schemas from your schema.py file
# from app.schema import Post, PostUpdate, UserCreate
# from app.utils import hash_password

# from .database import engine, Base, get_db
# from . import models

# # Tell SQLAlchemy to automatically build your PostgreSQL tables if they don't exist yet
# models.Base.metadata.create_all(bind=engine)


# app = FastAPI()

# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastAPI",
#         user="postgres",
#         password="1234",
#         cursor_factory=RealDictCursor
#     )
#     cursor = conn.cursor()
#     print("Database connection was successfull")
# except Exception as error:
#     print("Connection to database failed")
#     print("Error: ", error)
#     time.sleep(2)
    

# @app.get("/")
# async def root():
#     return {"message": "HelloJII World"}


# # --- 1. Get All Posts (Uses response_model list mapping) ---
# @app.get("/posts", status_code=status.HTTP_200_OK, response_model=list[Post])
# async def get_posts(db: Session = Depends(get_db)):
#     statement = select(models.Post)
#     posts = db.scalars(statement).all()
#     return posts # Return the flat list directly


# @app.get("/postgres")
# async def user_post():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}


# @app.post("/posts/trial", status_code=status.HTTP_201_CREATED, response_model=Post)
# async def create_post(new_post: Post, db: Session = Depends(get_db)):

#     db_post = models.Post(**new_post.model_dump())
    
#     db.add(db_post)     
#     db.commit()          
#     db.refresh(db_post)   
    
#     return db_post 


# @app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
# async def get_post(id: int, db: Session = Depends(get_db)):
#     statement = select(models.Post).where(models.Post.id == id)
#     result = db.scalars(statement).first()
    
#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"Post with ID {id} was not found"
#         )
        
#     return result 


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int, db: Session = Depends(get_db)):
#     statement = delete(models.Post).where(models.Post.id == id)
#     result = db.execute(statement)
    
#     if result.rowcount == 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist"
#         )
    
#     db.commit()
#     return None



# @app.patch("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
# async def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db)):
#     update_data = updated_post.model_dump(exclude_unset=True)
    
#     if not update_data:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="At least one field must be provided for update"
#         )

#     statement = (
#         update(models.Post)
#         .where(models.Post.id == id)
#         .values(**update_data)
#         .returning(models.Post)
#     )
#     result = db.execute(statement)
#     updated_record = result.scalar_one_or_none()
    
#     if not updated_record:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist"
#         )
    
#     db.commit()
#     return updated_record


# @app.post("/createUser", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):


#     user.password = hash_password(user.password)

    

#     new_user = models.User(**user.model_dump())

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return new_user











# from fastapi import Body, Depends, FastAPI, HTTPException, status
# from pydantic import BaseModel
# from typing import Optional;
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# from sqlalchemy import delete, select, update
# from sqlalchemy.orm import Session

# from app.schema import PostUpdate

# from .database import engine, Base, get_db
# from . import models

# # Tell SQLAlchemy to automatically build your PostgreSQL tables if they don't exist yet
# models.Base.metadata.create_all(bind=engine)


# app = FastAPI()



# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastAPI",
#         user="postgres",
#         password="1234",
#         cursor_factory=RealDictCursor
#     )

#     cursor = conn.cursor()
#     print("Database connection was successfull")

# except Exception as error:
#     print("Connection to database failed")
#     print("Error: ", error)
#     time.sleep(2)
    

# @app.get("/")
# async def root():
#     return {"message": "HelloJII World"}


# @app.get("/posts", status_code=status.HTTP_200_OK)
# async def get_posts(db: Session = Depends(get_db)):
#     statement = select(models.Post)
#     posts = db.scalars(statement).all()
#     return {"data": posts}

# @app.get("/postgres")
# async def user_post():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}

# # @app.post("/posts/trial", status_code= status.HTTP_201_CREATED)
# # async def create_post(new_post: Post):
# #     # print(new_post.model_dump())
# #     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
# #     result_post = cursor.fetchone()

# #     conn.commit()
# #     return {"new_data": result_post }

# @app.post("/posts/trial", status_code=status.HTTP_201_CREATED)
# async def create_post(new_post: models.Post, db: Session = Depends(get_db)):

#     db_post = models.Post(**new_post.model_dump())
    
#     db.add(db_post)     
#     db.commit()          
#     db.refresh(db_post)   
    
#     return {"new_data": db_post}



# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# async def get_post(id: int, db: Session = Depends(get_db)):
#     statement = select(models.Post).where(models.Post.id == id)
#     result = db.scalars(statement).first()
    
#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"Post with ID {id} was not found"
#         )
        
#     return {"post_details": result}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int, db: Session = Depends(get_db)):
#     statement = delete(models.Post).where(models.Post.id == id)
#     result = db.execute(statement)
    
#     if result.rowcount == 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist"
#         )
    
#     db.commit()
#     return None


# @app.patch("/posts/{id}", status_code=status.HTTP_200_OK, response_model = models.Post)
# async def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db)):
    
  
#     update_data = updated_post.model_dump(exclude_unset=True)
    
#     if not update_data:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="At least one field must be provided for update"
#         )

#     statement = (
#         update(models.Post)
#         .where(models.Post.id == id)
#         .values(**update_data)
#         .returning(models.Post)
#     )
#     result = db.execute(statement)
#     updated_record = result.scalar_one_or_none()
    
#     if not updated_record:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist"
#         )
    
#     db.commit()
#     return  updated_record

# # @app.get("/posts/{id}")
# # async def get_post(id: int):

# #     if id is None:
# #         raise HttpException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    
# #     print(id)
# #     cursor.execute(""" Select * from posts where id = %s """, (id,))

# #     result = cursor.fetchone()
# #     # conn.commit()
# #     print(result)
    
# #     return {"post": f"Here is the ID: {id} and result from DB: {result}" }