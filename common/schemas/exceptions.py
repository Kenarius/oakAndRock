from datetime import datetime

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    message: str
    code_error: str
    time: datetime
