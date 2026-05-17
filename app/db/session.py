from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import all models to register them with Base.metadata
# This ensures the engine knows about all tables and relationships
from app.models.user import User
from app.models.api_key import APIKey
from app.models.job import Job