import uuid as _uuid

from common.core.router import APIRouter
from common.db import get_async_session
from common.schemas.catalog import CatalogSchema
from common.schemas.category import DetailCategorySchema, ShortCategorySchema, CatalogsAndCategoriesResponse
from src.providers.catalog import provide_catalog_service
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
    response_model=CatalogsAndCategoriesResponse,
)
async def get_all_category() -> CatalogsAndCategoriesResponse:
    """GET category controller."""
    async with get_async_session() as session:
        service = provide_category_service(session)
        catalog_service = provide_catalog_service(session)
        catalogs = await catalog_service.get_all()
        categories = await service.get_all()
    parsed_categories = [
        ShortCategorySchema.model_validate(category, from_attributes=True) for category in categories
    ]
    parsed_catalogs = [
        CatalogSchema.model_validate(catalog, from_attributes=True) for catalog in catalogs
    ]
    return CatalogsAndCategoriesResponse(
        categories=parsed_categories,
        catalogs=parsed_catalogs,
    )

@api_router.delete(
    "/{item_id}",
    status_code=204
)
async def delete_category_by_id(item_id: _uuid.UUID):
    """Delete category."""
    async with get_async_session() as session:
        service = provide_category_service(session)
        await service.delete_by_uuid(item_id)

    return
