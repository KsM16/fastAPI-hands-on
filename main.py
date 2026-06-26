from fastapi import Body, FastAPI
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

@app.post("/createposts")
async def create_post(new_post: Post):
    print(new_post)
    return {"new_data": f"Title is : {new_post.title} and Content is: {new_post.content}" }