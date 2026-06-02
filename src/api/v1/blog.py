from fastapi import Depends, UploadFile
from uuid import UUID

from common.core.router import APIRouter
from src.api.dependencies.auth import is_authorized
from common.db import get_async_session
from common.schemas.blog import BlogSchema
from src.providers.blog import provide_blog_service

api_router = APIRouter()


@api_router.get(
    "/",
    response_model=list[BlogSchema],
)
async def get_all_blogs() -> list[BlogSchema]:
    """GET blog controller."""
    async with get_async_session() as session:
        service = provide_blog_service(session)
        blogs = await service.get_all()
        parsed_category = [
            BlogSchema.model_validate(blog, from_attributes=True) for blog in blogs
        ]
    return parsed_category


@api_router.post(
    "/",
    response_model=BlogSchema,
    dependencies=[Depends(is_authorized)],
)
async def create_blog(
        title: str,
        paragraph: str,
        description: str,
        first_image: UploadFile | None,
        second_image: UploadFile | None
) -> BlogSchema:
    data = {"title": title, "paragraph": paragraph, "description": description,
            "first_image": first_image, "second_image": second_image}
    async with get_async_session() as session:
        service = provide_blog_service(session)
        blog = await service.create(data)
    return BlogSchema.model_validate(blog, from_attributes=True)


@api_router.patch(
    "/{blog_id}",
    response_model=BlogSchema,
    dependencies=[Depends(is_authorized)],
)
async def update_blog(
        blog_id: UUID,
        title: str | None = None,
        paragraph: str | None = None,
        description: str | None = None,
        first_image: UploadFile | None = None,
        second_image: UploadFile | None = None
) -> BlogSchema:
    data = {"title": title, "paragraph": paragraph, "description": description,
            "first_image": first_image, "second_image": second_image}
    async with get_async_session() as session:
        service = provide_blog_service(session)
        blog = await service.update(blog_id, data)
    return BlogSchema.model_validate(blog, from_attributes=True)

@api_router.delete(
    "/{item_id}",
    status_code=204,
    dependencies=[Depends(is_authorized)],
)
async def delete_blog_by_id(item_id: UUID):
    """Delete blog."""
    async with get_async_session() as session:
        service = provide_blog_service(session)
        await service.delete_by_uuid(item_id)

    return
