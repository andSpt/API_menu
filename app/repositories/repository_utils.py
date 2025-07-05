import hashlib
import time
from typing import NoReturn

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def not_found(name: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found"
    )


def already_exist(name: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail=f"{name} already exists"
    )


def successfully_deleted(name: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": True, "message": f"The {name} has been deleted"},
    )


def generate_confirmation_token(email: str) -> str:
    timestamp = int(time.time())
    data: bytes = (email + str(timestamp)).encode()
    return hashlib.sha256(data).hexdigest()
