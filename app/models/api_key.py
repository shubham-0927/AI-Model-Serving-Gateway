from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from app.db.base import Base
import uuid
from datetime import datetime

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    key_prefix = Column(String, index=True)
    key_hash = Column(String)

    tier = Column(String, default="free")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
