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

    @property
    def admin_id(self) -> PydanticObjectId | None:
        """
        Propriedade que normaliza a referência ao admin.
        Se o link já foi resolvido, retorna admin.id; se for apenas o id, retorna direto.
        Usar fetch_link antes de converter para o schema garante comportamento consistente.
        """
        admin = getattr(self, "admin", None)
        if admin is None:
            return None
        # Admin document carregado
        if hasattr(admin, "id"):
            return admin.id
        # já é um ObjectId / string
        if isinstance(admin, (PydanticObjectId, str)):
            return admin
        return None

class LivroRead(BaseModel):
    id: PydanticObjectId | None = None
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    admin_id: PydanticObjectId | None = None

    # permite criar o schema a partir de atributos do Document (bom padrão)
    model_config = {
        "from_attributes": True,
    }

