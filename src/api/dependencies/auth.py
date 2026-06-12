"""API authorization dependencies."""
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from common.core.exceptions.domain import AuthenticationException
from common.core.security import decode_access_token

_bearer_scheme = HTTPBearer(auto_error=False)


async def is_authorized(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> str:
    """Require a valid admin Bearer token. Returns the authenticated username."""
    if credentials is None:
        raise AuthenticationException(detail="Authorization header is missing")
    username = decode_access_token(credentials.credentials)
    if username is None:
        raise AuthenticationException(detail="Invalid or expired token")
    return username
