from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel
from models.admin import Admin 

class LivroCreate(BaseModel):
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    admin_id: PydanticObjectId 

class LivroUpdate(BaseModel):
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None

class LivroRead(BaseModel):
    id: PydanticObjectId | None = None
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    
    model_config = { "from_attributes": True }

class Livro(Document):
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    
    admin: Link[Admin] 

    class Settings:
        name = "livro"

from models.admin import AdminComLivros
AdminComLivros.model_rebuild()