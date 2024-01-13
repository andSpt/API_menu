from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.routers import menu, dish, submenu
from app.models import Base
from app.database import engine




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.create_all)
    yield
    


app = FastAPI(lifespan=lifespan)


app.include_router(menu.router)
app.include_router(dish.router)
app.include_router(submenu.router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8040)


