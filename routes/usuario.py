from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.usuario import UsuarioCreate, UsuarioRead, Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/", response_model=Page[Usuario])
async def get_users() -> Page[UsuarioRead]:
    return await apaginate(Usuario.find_all())


@router.get("/{user_id}", response_model=Page[UsuarioRead])
async def get_users(user_id: PydanticObjectId) -> UsuarioRead:
    user = await UsuarioRead.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return UsuarioRead

@router.post("/", response_model=Usuario)
async def create_user(user: UsuarioCreate) -> Usuario:
    novo_usuario = Usuario(**user.model_dump())
    await novo_usuario.insert()
    return novo_usuario