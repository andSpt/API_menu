from fastapi import FastAPI
import uvicorn

from app.routers import menu, dish, submenu
from app.models import Base
from app.database import engine


app = FastAPI()


app.include_router(menu.router)
app.include_router(dish.router)
app.include_router(submenu.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8040)
