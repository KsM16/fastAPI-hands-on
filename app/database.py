from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# 1. Database URL configuration (Using SQLite for local development)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/fastAPI"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Create the modern 2.0 declarative base class for your models
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db  # Provides the active session connection context to the route
    finally:
        db.close() 