from common.core.router import APIRouter
from src.api.v1.category import api_router as category_router
from src.api.v1.item import api_router as item_router

router = APIRouter()
router.include_router(category_router, prefix="/categories", tags=["categories"])
router.include_router(item_router, prefix="/items", tags=["items"])
