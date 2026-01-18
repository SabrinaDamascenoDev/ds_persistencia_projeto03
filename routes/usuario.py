from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.usuario import Usuario, UsuarioCreate, UsuarioRead
from beanie.operators import RegEx
import re

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.get("/", response_model=Page[UsuarioRead])
async def get_users(
    nome: str | None = Query(None, description="Filtrar por nome (parcial)")
):
    query = Usuario.find_all()

    if nome:
        query = query.find(
            RegEx(Usuario.nome, re.compile(nome, re.IGNORECASE))
        )

    return await apaginate(query)

@router.get("/{user_id}", response_model=UsuarioRead)
async def get_user(user_id: PydanticObjectId):
    user = await Usuario.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=UsuarioRead, status_code=201)
async def create_user(user: UsuarioCreate):
    novo_usuario = Usuario(**user.model_dump())
    await novo_usuario.insert()
    return novo_usuario


@router.put("/{user_id}", response_model=UsuarioRead)
async def update_user(user_id: PydanticObjectId, user_in: UsuarioCreate):
    user = await Usuario.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    await user.set(user_in.model_dump(exclude_unset=True))
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: PydanticObjectId):
    user = await Usuario.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    await user.delete()
    return None
