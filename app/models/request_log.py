from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.db.base import Base
from datetime import datetime
import uuid

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"))
    api_key_id = Column(String, ForeignKey("api_keys.id"))

    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)

    latency_ms = Column(Integer)

    tokens_used = Column(Integer, default=0)

    job_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)