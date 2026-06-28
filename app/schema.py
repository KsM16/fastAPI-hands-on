from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic import Field, field_validator


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

    model_config = ConfigDict(from_attributes=True) 

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., description="1 to upvote, 0 to remove vote")

    @field_validator('dir')
    @classmethod
    def validate_dir(cls, v: int) -> int:
        if v not in (0, 1):
            raise ValueError("dir must be 0 or 1")
        return v