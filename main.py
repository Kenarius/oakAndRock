"""Startup package for microservice."""
import logging
import os
import sys

import uvicorn
from fastapi import FastAPI, Request
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from common.conf.config_swagger import get_swagger_config
from common.conf.settings import settings
from common.core.enums import ServiceEnum
from common.core.exceptions.exception_handlers import add_exception_handlers
from common.db.engine import get_engine
from src.admin.auth import AdminAuthBackend
from src.api.router import api_router
from src.admin.views import CategoryAdmin, ItemAdmin, CatalogAdmin, BlogAdmin

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_uncaught_exception


def init_app() -> FastAPI:
    """Create FastAPI app."""
    app = FastAPI(**get_swagger_config(ServiceEnum.OAK))
    session_secret = settings.admin_auth.session_secret
    app.add_middleware(SessionMiddleware, secret_key=session_secret)
    engine = get_engine(
        settings.postgres.db_uri,
        echo=settings.postgres.echo,
    )
    admin_auth = AdminAuthBackend(session_secret)
    admin = Admin(app, engine, base_url="/oak/admin", authentication_backend=admin_auth)
    admin.add_view(CategoryAdmin)
    admin.add_view(ItemAdmin)
    admin.add_view(CatalogAdmin)
    admin.add_view(BlogAdmin)

    app.include_router(api_router)
    add_exception_handlers(app=app)

    @app.middleware("http")
    async def log_exceptions(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            logger.exception("Unhandled error on %s %s", request.method, request.url.path)
            raise

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:init_app",
        host=os.getenv("SERVICE_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVICE_PORT", 10000)),
        reload=False,
        factory=True,
        log_level="debug"
    )
