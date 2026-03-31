from datetime import datetime

from sqlalchemy import UUID, text, func, String
from sqlalchemy.orm import mapped_column, Mapped


class UUIDMixin:
    """Identifier uuid mixin."""

    uuid: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))


class TimestampMixin:
    """Timestamp mixin."""

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class TitleMixin:
    """Title mixin."""

    title: Mapped[str] = mapped_column(String(255))
    paragraph: Mapped[str] = mapped_column(String(255))
