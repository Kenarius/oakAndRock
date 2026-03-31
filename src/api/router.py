from common.core.router import APIRouter
from src.api.v1.router import router as api_v1_router

api_router = APIRouter(prefix="/api")
api_router.include_router(api_v1_router, prefix="/v1")
