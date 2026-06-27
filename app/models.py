from datetime import datetime
from typing import Optional
from sqlalchemy import String, text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base   
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column()

    content: Mapped[str] = mapped_column()

    published: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), 
        server_default=text("now()")
    )

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(unique=True, index=True)

    password: Mapped[str] = mapped_column(nullable=False)

    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), 
        server_default=text("now()")
    )
