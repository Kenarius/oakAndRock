"""Admin authentication service."""
from common.core.exceptions.domain import AuthenticationException
from common.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_admin_credentials,
)


class AuthService:
    """Authenticate admin users and issue access tokens."""

    def login(self, username: str, password: str) -> tuple[str, str]:
        if not verify_admin_credentials(username, password):
            raise AuthenticationException(detail="Invalid username or password")
        return (
            create_access_token(subject=username),
            create_refresh_token(subject=username),
        )

    def refresh(self, refresh_token: str) -> tuple[str, str]:
        username = decode_refresh_token(refresh_token)
        if username is None:
            raise AuthenticationException(detail="Invalid or expired refresh token")
        return (
            create_access_token(subject=username),
            create_refresh_token(subject=username),
        )
