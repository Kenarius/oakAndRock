"""Domain exceptions."""

from common.core.exceptions.base import DomainException


class AuthorizationException(DomainException):
    DEFAULT_ERROR_MESSAGE = "You don't have enough permissions to perform that action."
    DEFAULT_ERROR_CODE = "permission_denied"
    DEFAULT_STATUS_CODE = 403


class AuthenticationException(DomainException):
    DEFAULT_ERROR_MESSAGE = "Authentication failed."
    DEFAULT_ERROR_CODE = "auth_failed"
    DEFAULT_STATUS_CODE = 401


class EmailIsNotProvidedOAuthException(DomainException):
    DEFAULT_ERROR_MESSAGE = "Email is not provided."
    DEFAULT_ERROR_CODE = "email_not_provided"
    DEFAULT_STATUS_CODE = 400

    def __init__(self, headers: dict = None, detail: str | None = None, status_code: int | None = None):
        super().__init__(detail=detail, status_code=status_code)
        self.headers = headers
