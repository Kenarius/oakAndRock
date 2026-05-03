from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = hashlib.sha256(
    os.getenv("ADMIN_PASSWORD", "password").encode()
).hexdigest()
SESSION_SECRET = os.getenv("ADMIN_SESSION_SECRET", "default_secret")


class AdminAuthBackend(AuthenticationBackend):
    """Класс авторизации для SQLAdmin"""

    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        """Проверка логина"""
        if request.session.get("admin_authenticated"):
            return True

        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Твоя проверка из .env
        if (username == ADMIN_USERNAME and
                hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH):
            request.session["admin_authenticated"] = True
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Выход"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверка авторизации"""
        return request.session.get("admin_authenticated", False)