from fastapi import APIRouter


router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])