from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from common.db import BaseModel, UUIDMixin, TimestampMixin, TitleMixin


class Blog(BaseModel, UUIDMixin, TimestampMixin, TitleMixin):
    """Blog model definition."""

    __tablename__ = "blog"

    description: Mapped[str] = mapped_column(Text)
    first_media_url: Mapped[str] = mapped_column(String(5000))
    second_media_url: Mapped[str] = mapped_column(String(5000))
