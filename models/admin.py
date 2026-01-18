from typing import List, TYPE_CHECKING
from beanie import Document
from pydantic import BaseModel
from beanie.odm.fields import PydanticObjectId

if TYPE_CHECKING:
    from models.livro import LivroRead

class AdminCreate(BaseModel):
    nome: str | None = None
    email: str | None = None

class AdminUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None

class Admin(Document):
    nome: str | None = None
    email: str | None = None

    class Settings:
        name = "admin"

class AdminComLivros(BaseModel):
    id: PydanticObjectId
    nome: str | None
    email: str | None
    livros_adicionados: List["LivroRead"] = []