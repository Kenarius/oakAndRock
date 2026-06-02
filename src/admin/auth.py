from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from common.conf.settings import settings
from common.core.security import verify_admin_credentials


class AdminAuthBackend(AuthenticationBackend):
    """SQLAdmin session authentication using credentials from .env."""

    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        if request.session.get("admin_authenticated"):
            return True

        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if isinstance(username, str) and isinstance(password, str):
            if verify_admin_credentials(username, password):
                request.session["admin_authenticated"] = True
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_authenticated", False)
