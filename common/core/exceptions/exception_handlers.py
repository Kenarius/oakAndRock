from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import UJSONResponse
from sqlalchemy.exc import IntegrityError

from common.core.exceptions.api_exception import ApiException
from common.core.exceptions.base import (
    BadRequestError,
    DomainException,
    ForbiddenError,
    InfrastructureException,
    NotFoundError,
    UnauthorizedError,
    ValuePydanticError,
)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(DomainException)
    def domain_exception_handler(request: Request, exc: DomainException) -> UJSONResponse:
        """Handling domain exception."""
        return UJSONResponse(content={"detail": exc.detail, "error_code": exc.error_code}, status_code=exc.status_code)

    @app.exception_handler(InfrastructureException)
    def infrastructure_exception_handler(request: Request, exc: InfrastructureException) -> UJSONResponse:
        """Handling infra exception."""
        return UJSONResponse(content={"detail": exc.detail, "error_code": exc.error_code}, status_code=exc.status_code)

    @app.exception_handler(Exception)
    def unknown_error_exception_handler(request: Request, exc: Exception) -> UJSONResponse:
        """Handling unknown exception."""
        return UJSONResponse(content={"detail": "Unexpected error occurred"}, status_code=500)

    @app.exception_handler(IntegrityError)
    def integrity_exception_handler(request: Request, exc: IntegrityError) -> UJSONResponse:
        """Handling integrity exception."""
        return UJSONResponse(content={"detail": str(exc.orig).split("DETAIL:  ")[-1]}, status_code=409)

    @app.exception_handler(ApiException)
    async def unicorn_exception_handler(request: Request, exc: ApiException):
        return UJSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(
            request: Request,
            exc: NotFoundError,
            status_code: status = status.HTTP_404_NOT_FOUND,
    ):
        return UJSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_exception_handler(
            request: Request,
            exc: UnauthorizedError,
            status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        return UJSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ValuePydanticError)
    async def value_error_exception_handler(
            request: Request,
            exc: ValuePydanticError,
            status_code: status = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        return UJSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden_error_exception_handler(
            request: Request,
            exc: ForbiddenError,
            status_code: status = status.HTTP_403_FORBIDDEN,
    ):
        return UJSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_error_exception_handler(
            request: Request,
            exc: BadRequestError,
            status_code: status = status.HTTP_400_BAD_REQUEST,
    ):
        return UJSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(DomainException)
    def email_is_not_provided_from_oauth(request: Request, exc: DomainException) -> UJSONResponse:
        """Handling domain exception."""
        try:
            headers = exc.headers   # noqa
        except AttributeError:
            headers = None
        return UJSONResponse(
            content={"detail": exc.detail, "error_code": exc.error_code},
            status_code=exc.status_code,
            headers=headers,
        )
