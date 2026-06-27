from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Post(BaseModel):
    title: str               
    content: str                
    published: bool = True    

    model_config = ConfigDict(from_attributes=True)  

class PostUpdate(BaseModel):
    title: Optional[str] = None         
    content: Optional[str] = None     
    published: Optional[bool] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str