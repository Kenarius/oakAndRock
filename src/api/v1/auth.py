from common.core.router import APIRouter
from common.schemas.auth import LoginRequest, TokenResponse
from src.providers.auth import provide_auth_service

api_router = APIRouter()


@api_router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest) -> TokenResponse:
    """Authenticate admin and return a JWT access token."""
    service = provide_auth_service()
    access_token = service.login(body.username, body.password)
    return TokenResponse(access_token=access_token)
