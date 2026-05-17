import secrets
import hashlib

from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from datetime import datetime

def generate_api_key():
    key = "sk-" + secrets.token_urlsafe(32)
    return key

def get_prefix(key: str):
    return key[3:10]  # skip "sk-"

def hash_key(key: str):
    return hashlib.sha256(key.encode()).hexdigest()

def create_api_key(db: Session, user_id: str, tier = "free"):
    key = generate_api_key()
    prefix = get_prefix(key)
    key_hash = hash_key(key)
    
    if tier not in ["free", "pro"]:
        raise Exception("Invalid tier")
    
    api_key = APIKey(
        user_id=user_id,
        key_prefix=prefix,
        key_hash=key_hash,
        tier=tier
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return key, api_key