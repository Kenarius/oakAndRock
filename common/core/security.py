"""Admin credentials and JWT helpers."""
import hashlib
from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

from common.conf.settings import settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_admin_credentials(username: str, password: str) -> bool:
    auth = settings.admin_auth
    return username == auth.username and hash_password(password) == hash_password(auth.password)


def create_access_token(subject: str) -> str:
    auth = settings.admin_auth
    expire = datetime.now(timezone.utc) + timedelta(minutes=auth.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, auth.effective_jwt_secret, algorithm=auth.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    auth = settings.admin_auth
    try:
        payload = jwt.decode(
            token,
            auth.effective_jwt_secret,
            algorithms=[auth.jwt_algorithm],
        )
    except InvalidTokenError:
        return None
    if payload.get("type") != "access":
        return None
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None
