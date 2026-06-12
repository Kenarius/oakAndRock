"""Admin credentials and JWT helpers."""
import hashlib
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from jwt import InvalidTokenError

from common.conf.settings import settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_admin_credentials(username: str, password: str) -> bool:
    auth = settings.admin_auth
    return username == auth.username and hash_password(password) == hash_password(auth.password)


def _create_token(*, subject: str, token_type: str, expire_minutes: int) -> str:
    auth = settings.admin_auth
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": token_type,
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, auth.effective_jwt_secret, algorithm=auth.jwt_algorithm)


def _decode_token(*, token: str, expected_type: str) -> str | None:
    auth = settings.admin_auth
    try:
        payload = jwt.decode(
            token,
            auth.effective_jwt_secret,
            algorithms=[auth.jwt_algorithm],
        )
    except InvalidTokenError:
        return None
    if payload.get("type") != expected_type:
        return None
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None


def create_access_token(subject: str) -> str:
    auth = settings.admin_auth
    return _create_token(
        subject=subject,
        token_type="access",
        expire_minutes=auth.access_token_expire_minutes,
    )


def create_refresh_token(subject: str) -> str:
    auth = settings.admin_auth
    return _create_token(
        subject=subject,
        token_type="refresh",
        expire_minutes=auth.refresh_token_expire_minutes,
    )


def decode_access_token(token: str) -> str | None:
    return _decode_token(token=token, expected_type="access")


def decode_refresh_token(token: str) -> str | None:
    return _decode_token(token=token, expected_type="refresh")
