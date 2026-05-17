from app.db.base import Base
from app.db.session import engine

# Import all models to ensure they are registered with Base.metadata
# Order matters - import dependencies first
from app.models.user import User
from app.models.api_key import APIKey
from app.models.job import Job
from app.models.request_log import RequestLog

def init_db():
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)