"""Startup package for microservice."""
import os

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from common.conf.config_swagger import get_swagger_config
from common.conf.settings import settings
from common.core.enums import ServiceEnum
from common.core.exceptions.exception_handlers import add_exception_handlers
from common.db.engine import get_engine
from src.api.router import api_router
from src.admin.views import CategoryAdmin, ItemAdmin


def init_app() -> FastAPI:
    """Create FastAPI app."""
    app = FastAPI(**get_swagger_config(ServiceEnum.OAK))

    engine = get_engine(
        settings.postgres.db_uri,
        echo=settings.postgres.echo,
    )
    admin = Admin(app, engine, base_url="/oak/admin")
    admin.add_view(CategoryAdmin)
    admin.add_view(ItemAdmin)

    app.include_router(api_router)
    add_exception_handlers(app=app)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:init_app",
        host=os.getenv("SERVICE_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVICE_PORT", 8000)),
        reload=True,
        factory=True,
    )
