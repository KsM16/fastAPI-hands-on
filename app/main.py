from fastapi import Body, FastAPI, status
from pydantic import BaseModel
from typing import Optional;
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastAPI",
        user="postgres",
        password="1234",
        cursor_factory=RealDictCursor
    )

    cursor = conn.cursor()
    print("Database connection was successfull")

except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)
    time.sleep(2)
    

@app.get("/")
async def root():
    return {"message": "HelloJII World"}

@app.get("/postgres")
async def user_post():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts/trial", status_code= status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    # print(new_post.model_dump())
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    result_post = cursor.fetchone()

    conn.commit()
    return {"new_data": result_post }

@app.get("/posts/{id}")
async def get_post(id: int):

    if id is None:
        raise HttpException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    print(id)
    cursor.execute(""" Select * from posts where id = %s """, (id,))

    result = cursor.fetchone()
    # conn.commit()
    print(result)
    
    return {"post": f"Here is the ID: {id} and result from DB: {result}" }