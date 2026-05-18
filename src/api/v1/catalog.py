from uuid import UUID

from httpx import Response

from common.core.router import APIRouter
from common.db import get_async_session
from common.schemas.catalog import CatalogSchema
from src.providers.catalog import provide_catalog_service

api_router = APIRouter()

@api_router.get(
    "/",
    response_model=list[CatalogSchema],
)
async def get_all_catalogs() -> list[CatalogSchema]:
    """GET catalog controller."""
    async with get_async_session() as session:
        service = provide_catalog_service(session)
        catalogs = await service.get_all()
        parsed_category = [
            CatalogSchema.model_validate(catalog, from_attributes=True) for catalog in catalogs
        ]
    return parsed_category

@api_router.delete(
    "/{item_id}",
    status_code=204
)
async def delete_catalog_by_id(item_id: UUID):
    """Delete catalog."""
    async with get_async_session() as session:
        service = provide_catalog_service(session)
        await service.delete_by_uuid(item_id)

    return
