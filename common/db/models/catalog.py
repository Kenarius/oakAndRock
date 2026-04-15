from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from common.db import BaseModel, UUIDMixin, TimestampMixin


class Catalog(BaseModel, UUIDMixin, TimestampMixin):
    """Catalog model definition."""

    __tablename__ = "catalog"

    title: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(Text)
    pdf_url: Mapped[str] = mapped_column(String(500))
