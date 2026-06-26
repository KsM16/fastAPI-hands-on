from fastapi import Body, FastAPI, status
from pydantic import BaseModel
from typing import Optional;

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "HelloJII World"}

@app.get("/posts")
async def user_post():
    return {"data": "User post !!!!!!"}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    print(new_post.model_dump())
    return {"new_data": new_post }

@app.get("/posts/{id}")
async def get_post(id: int):
    print(id)
    if id is None:
        raise HttpException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post": f"Here is the ID: {id}" }