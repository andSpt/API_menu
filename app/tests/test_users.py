from uuid import UUID

import pytest
from fastapi import HTTPException
from models import User
from schemas import UserResponse
from sqlalchemy import select
from sqlalchemy.engine import Result

BASE_URL = "/api/v1/users"


@pytest.mark.order(1)
async def test_get_all_users(client, async_test_session):
    response = await client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == []

    stmt = select(User)
    result: Result = await async_test_session.execute(stmt)
    list_users = [
        UserResponse.model_validate(row, from_attributes=True) for row in result
    ]
    assert list_users == []
