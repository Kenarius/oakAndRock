from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import BaseModel, UUIDMixin, TimestampMixin, TitleMixin

if TYPE_CHECKING:
    from common.db.models.item import Item


class Category(BaseModel, UUIDMixin, TimestampMixin, TitleMixin):
    """Category model definition."""

    __tablename__ = "category"

    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    main_media_url: Mapped[str] = mapped_column(String(500))
    first_media_url: Mapped[str] = mapped_column(String(500))
    second_media_url: Mapped[str] = mapped_column(String(500))
    marks: Mapped[list] = mapped_column(JSONB, nullable=True, server_default="[]")

    items: Mapped[list["Item"]] = relationship(
        back_populates="category",
        lazy="selectin",
    )
