from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel


class Usuario(Document):
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None

    class Settings:
        name = "usuario"


class UsuarioCreate(BaseModel):
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None


class UsuarioRead(BaseModel):
    id: PydanticObjectId
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,   
    }
