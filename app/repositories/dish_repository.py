from uuid import UUID

import sqlalchemy

from sqlalchemy.orm import selectinload
from app.models import Dish, Submenu, Menu