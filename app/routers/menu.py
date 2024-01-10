from fastapi import APIRouter


router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.get('/')
async def get_list_menus():
    pass


@router.get('/{menu_id}')
async def get_menu():
    pass


@router.post('/')
async def create_menu():
    pass


@router.patch('/{menu_id}')
async def update_menu():
    pass


@router.delete('/{menu_id}')
async def delete_menu():
    pass
