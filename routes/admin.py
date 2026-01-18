from typing import Any
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.admin import Admin, AdminCreate, Admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/", response_model=list[Admin])
async def get_admins(skip: int = 0, limit: int = 10):
    admins = await Admin.find_all(fetch_links=True).skip(skip).limit(limit).to_list()
    
    if not admins:
        raise HTTPException(status_code=404, detail="Nenhum admin encontrado")
    return admins

@router.get("/{admin_id}", response_model=Admin)
async def get_admin(admin_id: PydanticObjectId) -> Any:
    admin = await Admin.get(admin_id, fetch_links=True)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin


@router.post("/", response_model=Admin)
async def create_admin(admin: AdminCreate) -> Admin:
    novo_admin = Admin(**admin.model_dump())
    await novo_admin.insert()
    return novo_admin