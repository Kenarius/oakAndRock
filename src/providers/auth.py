from src.services.auth import AuthService


def provide_auth_service() -> AuthService:
    return AuthService()
