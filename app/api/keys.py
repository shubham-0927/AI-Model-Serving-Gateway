from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.key_service import create_api_key


router = APIRouter(prefix="/keys", tags=["api-keys"])


@router.post("/")
def generate_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    key, _ = create_api_key(db, current_user.id)

    return {
        "api_key": key,
        "message": "Store this key securely🤫. It won't be shown again."
    }