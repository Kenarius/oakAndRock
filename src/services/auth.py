"""Admin authentication service."""
from common.core.exceptions.domain import AuthenticationException
from common.core.security import create_access_token, verify_admin_credentials


class AuthService:
    """Authenticate admin users and issue access tokens."""

    def login(self, username: str, password: str) -> str:
        if not verify_admin_credentials(username, password):
            raise AuthenticationException(detail="Invalid username or password")
        return create_access_token(subject=username)
