from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base import Base
import uuid
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"))
    api_key_id = Column(String, ForeignKey("api_keys.id"))

    status = Column(String, default="queued")  # queued, running, completed, failed

    input_data = Column(String, nullable=True)
    output_data = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)