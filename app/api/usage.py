from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.api_key_auth import get_api_key
from app.models.api_key import APIKey
from app.models.request_log import RequestLog
router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("/")
def get_usage(
    api_key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    total_requests = db.query(func.count(RequestLog.id)).filter(
        RequestLog.api_key_id == api_key.id
    ).scalar()
    total_tokens = db.query(func.sum(RequestLog.tokens_used)).filter(
        RequestLog.api_key_id == api_key.id
    ).scalar()
    return {
        "total_requests": total_requests,
        "total_tokens": total_tokens or 0
    }