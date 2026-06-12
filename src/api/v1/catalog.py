from uuid import UUID

from fastapi import Depends, UploadFile

from common.core.router import APIRouter
from src.api.dependencies.auth import is_authorized
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

@api_router.post(
    "/",
    response_model=CatalogSchema,
    dependencies=[Depends(is_authorized)],
)
async def create_catalog(
        title: str,
        image_file: UploadFile,  # svg file
        pdf_file: UploadFile
) -> CatalogSchema:
    data = {"title": title, "image_file": image_file, "pdf_file": pdf_file}
    async with get_async_session() as session:
        service = provide_catalog_service(session)
        catalog = await service.create(data)
    return CatalogSchema.model_validate(catalog, from_attributes=True)

@api_router.delete(
    "/{item_id}",
    status_code=204,
    dependencies=[Depends(is_authorized)],
)
async def delete_catalog_by_id(item_id: UUID):
    """Delete catalog."""
    async with get_async_session() as session:
        service = provide_catalog_service(session)
        await service.delete_by_uuid(item_id)

    return
