from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID

from common.db import BaseModel, UUIDMixin, TimestampMixin, TitleMixin


class Item(BaseModel, UUIDMixin, TimestampMixin, TitleMixin):
    """Item model definition."""

    __tablename__ = "item"

    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    subtitle: Mapped[str] = mapped_column(String(255), nullable=True, server_default="")
    main_media_url: Mapped[str] = mapped_column(String(500))
    media_urls: Mapped[list] = mapped_column(JSONB)
    description_marks: Mapped[list[list[str]]] = mapped_column(JSONB, nullable=True)
    marks: Mapped[list] = mapped_column(JSONB, nullable=True, server_default="[]")
    price: Mapped[str] = mapped_column(String(255))

    category_uuid: Mapped[str] = mapped_column(
        UUID,
        ForeignKey("category.uuid", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    category = relationship(
        "Category",
        back_populates="items",
        lazy="selectin",
    )
