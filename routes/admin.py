from typing import Any
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page, paginate
from models.admin import Admin, AdminCreate, AdminUpdate

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/", response_model=Page[Admin])
async def get_admins():
    """
    Lista admins com paginação.
    """
    query = Admin.find_all(fetch_links=True)

    return await paginate(query)

@router.get("/{admin_id}", response_model=Admin)
async def get_admin(admin_id: PydanticObjectId) -> Any:
    """
    Recupera um admin por ID.
    Retorna 404 se não encontrado.
    """
    admin = await Admin.get(admin_id, fetch_links=True)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin


@router.post("/", response_model=Admin, status_code=201)
async def create_admin(admin: AdminCreate) -> Admin:
    """
    Cria um novo admin. Validação de email e nome feita pelo Pydantic.
    """
    novo_admin = Admin(**admin.model_dump())
    await novo_admin.insert()
    return novo_admin

@router.put("/{admin_id}", response_model=Admin)
async def update_admin(admin_id: PydanticObjectId, admin_in: AdminUpdate):
    """
    Atualiza um admin parcial (patch-like) com campos opcionais.
    """
    admin = await Admin.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    await admin.set(admin_in.model_dump(exclude_unset=True))
    return admin

@router.delete("/{admin_id}", status_code=204)
async def delete_admin(admin_id: PydanticObjectId):
    """
    Remove um admin. Retorna 404 se não existir.
    """
    admin = await Admin.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    await admin.delete()
    return None