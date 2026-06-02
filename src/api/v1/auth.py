from common.core.router import APIRouter
from common.schemas.auth import LoginRequest, RefreshRequest, TokenPairResponse
from src.providers.auth import provide_auth_service

api_router = APIRouter()


@api_router.post("/login", response_model=TokenPairResponse)
async def login(body: LoginRequest) -> TokenPairResponse:
    """Authenticate admin and return access + refresh tokens."""
    service = provide_auth_service()
    access_token, refresh_token = service.login(body.username, body.password)
    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)


@api_router.post("/refresh", response_model=TokenPairResponse)
async def refresh(body: RefreshRequest) -> TokenPairResponse:
    """Rotate refresh token and return new token pair."""
    service = provide_auth_service()
    access_token, refresh_token = service.refresh(body.refresh_token)
    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)
