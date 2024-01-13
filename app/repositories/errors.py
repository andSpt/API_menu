from typing import NoReturn

from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result



def alredy_exist(name_subject: str) -> NoReturn:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'{name_subject} already exists')



# async def check_exists_object_by_attribute(model, object, attribute: str) -> None:
#         '''Функция проверяет существует ли в базе данных объект с данным атрибутом'''
        
#         stmt = select(model).where(model.attribute == object.attribute)
#         result: Result = await model.session.execute(stmt)
#         object = result.scalars().first()

#         if object:
#             alredy_exist(model.name)