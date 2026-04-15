from common.core.router import APIRouter
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
