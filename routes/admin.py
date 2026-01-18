from typing import Any
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.admin import Admin, AdminCreate, AdminComLivros

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/", response_model=Page[AdminComLivros])
async def get_admins() -> Page[AdminComLivros]:
    admins_page = await apaginate(Admin.find_all())
    if not admins_page.items:
        raise HTTPException(status_code=404, detail="Nenhum admin encontrado")
    return admins_page

@router.get("/{admin_id}", response_model=AdminComLivros)
async def get_admin(admin_id: PydanticObjectId) -> Any:
    admin = await Admin.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin

@router.get("/{admin_id}/livros", response_model=AdminComLivros)
async def get_admin_livros(admin_id: PydanticObjectId) -> Any:
    return await get_admin(admin_id)

@router.post("/", response_model=Admin)
async def create_admin(admin: AdminCreate) -> Admin:
    novo_admin = Admin(**admin.model_dump())
    await novo_admin.insert()
    return novo_admin