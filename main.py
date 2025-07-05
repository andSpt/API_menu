import uvicorn
from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import dish, menu, submenu, user

app = FastAPI()


app.include_router(menu.router)
app.include_router(dish.router)
app.include_router(submenu.router)
app.include_router(user.router)
app.include_router(user.router_jwt)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8040)
