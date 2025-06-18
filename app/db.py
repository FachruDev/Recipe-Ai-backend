# app/db.py
import os
from sqlmodel import SQLModel, create_engine, Session
from app.config import Settings

settings = Settings()

# Check if DATABASE_URL environment variable is set (Heroku sets this)
if os.environ.get("DATABASE_URL"):
    # Heroku uses PostgreSQL and provides DATABASE_URL
    # Note: Heroku's DATABASE_URL starts with postgres://, but SQLAlchemy requires postgresql://
    DATABASE_URL = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
else:
    # Local development uses SQLite
    DATABASE_URL = f"sqlite:///{settings.database_file}"

# Create engine with appropriate connect_args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args
)

def init_db():
    from app.models import SessionModel, MessageModel
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
