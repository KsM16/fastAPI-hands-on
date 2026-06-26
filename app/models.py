from datetime import datetime
from typing import Optional
from sqlalchemy import String, text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base  # Imports the Base from your database.py

class Post(Base):
    __tablename__ = "posts"

    # 1. id: integer, Primary Key, Not NULL, Auto-incrementing (nextval)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 2. title: character varying (VARCHAR), Not NULL
    title: Mapped[str] = mapped_column()

    # 3. content: character varying (VARCHAR), Not NULL
    content: Mapped[str] = mapped_column()

    # 4. published: boolean, Not NULL, Default value: true
    published: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    # 5. created: timestamp with time zone, Not NULL, Default value: now()
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), 
        server_default=text("now()")
    )
