import uuid as _uuid

from common.core.router import APIRouter
from common.db import get_async_session
from common.schemas.item import DetailItemSchema
from src.providers.item import provide_item_service

api_router = APIRouter()


@api_router.get(
    "/{uuid}",
    response_model=DetailItemSchema,
)
async def get_item(uuid: _uuid.UUID) -> DetailItemSchema:
    """GET item controller."""
    async with get_async_session() as session:
        service = provide_item_service(session)
        item = await service.get_by_uuid(uuid)
        parsed_item = DetailItemSchema.model_validate(item)
    return parsed_item
