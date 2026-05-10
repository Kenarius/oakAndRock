"""Blog service."""
import uuid

from common.core.utlis.images import upload_file_to_disk
from common.services.base import BaseCRUDService
from src.repositories.blog import BlogRepository


class BlogService(BaseCRUDService):
    """Encapsulates Blog logic."""
    
    def __init__(self, blog_repository: BlogRepository):
        """Initialize Blog service."""
        super().__init__(blog_repository)
        self._blog_repo = blog_repository

    async def create(self, data: dict):
        """Create obj."""
        first_media_url = None
        if data.get("first_image"):
            first_media_url = await upload_file_to_disk(data.get("first_image"), data["title"], "blog")

        second_media_url = None
        if data.get("second_image"):
            second_media_url = await upload_file_to_disk(data.get("second_image"), data["title"], "blog")

        blog_data = {
            "title": data["title"],
            "paragraph": data["paragraph"],
            "description": data["description"],
            "first_media_url": first_media_url or "",
            "second_media_url": second_media_url or "",
        }
        obj = await self._repository.create(blog_data)
        return obj

    async def update(self, uuid: uuid.UUID, data: dict):
        """Update by uuid."""
        blog_data = {}

        if data.get("first_image"):
            blog_data["first_media_url"] = await upload_file_to_disk(
                data.get("first_image"), data["title"], "blog"
            )

        if data.get("second_image"):
            blog_data["second_media_url"] = await upload_file_to_disk(
                data.get("second_image"), data["title"], "blog"
            )

        if "title" in data:
            blog_data["title"] = data["title"]

        if "paragraph" in data:
            blog_data["paragraph"] = data["paragraph"]

        if "description" in data:
            blog_data["description"] = data["description"]

        updated_data = {k: v for k, v in blog_data.items() if v is not None}
        result = await self._repository.update(uuid, updated_data)
        return result
