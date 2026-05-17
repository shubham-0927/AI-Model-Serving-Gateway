from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.api_key import APIKey
from app.services.key_service import hash_key


security = HTTPBearer()

def get_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # Check prefix
    if not token.startswith("sk-"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key format❌"
        )
    prefix = token[3:10]
    api_key = db.query(APIKey).filter(
        APIKey.key_prefix == prefix,
        APIKey.is_active == True
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key❌"
        )

    
    if api_key.key_hash != hash_key(token):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return api_key