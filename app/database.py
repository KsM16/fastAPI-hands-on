from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings   

 
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close()