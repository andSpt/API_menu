from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Base
from repositories.messages import already_exist
from typing import NoReturn

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result


def not_found(name: str) -> NoReturn:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'{name} not found')


def already_exist(name: str) -> NoReturn:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f'{name} already exists')


def successfully_deleted(name: str) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'status': True, 'message': f'The {name} has been deleted'})