import uuid as _uuid

from common.core.router import APIRouter
from common.db import get_async_session
from common.schemas.category import DetailCategorySchema, ShortCategorySchema
from src.providers.category import provide_category_service

api_router = APIRouter()

@api_router.get(
    "/{uuid}",
    response_model=DetailCategorySchema,
)
async def get_category(uuid: _uuid.UUID) -> DetailCategorySchema:
    """GET category controller."""
    async with get_async_session() as session:
        service = provide_category_service(session)
        category = await service.get_by_uuid(uuid)
        parsed_category = DetailCategorySchema.model_validate(category, from_attributes=True)
    return parsed_category

@api_router.get(
    "/",
    response_model=list[ShortCategorySchema],
)
async def get_all_category() -> list[ShortCategorySchema]:
    """GET category controller."""
    async with get_async_session() as session:
        service = provide_category_service(session)
        categories = await service.get_all()
        parsed_category = [
            ShortCategorySchema.model_validate(category, from_attributes=True) for category in categories
        ]
    return parsed_category
