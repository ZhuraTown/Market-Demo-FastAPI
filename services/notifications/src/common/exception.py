from dataclasses import dataclass
from http import HTTPStatus

from fastapi import HTTPException


class DBError(Exception):
    @property
    def message(self):
        return "Error while trying commit"


@dataclass
class ApplicationException(HTTPException):
    status_code: int
    detail: str


@dataclass
class BadTokenError(ApplicationException):
    status_code: int = HTTPStatus.UNAUTHORIZED
    detail: str = "Invalid token"
