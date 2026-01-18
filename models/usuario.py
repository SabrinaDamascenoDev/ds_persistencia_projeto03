from beanie import Document
from pydantic import Field
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
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None

