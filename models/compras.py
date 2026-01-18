from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field
from models.usuario import Usuario
from models.livro import Livro, LivroRead


class Compras(Document):
    usuario: Link[Usuario]
    livro: Link[Livro]
    quantidade: int = 1
    preco_total: float | None = None

    class Settings:
        name = "compras"

    @property
    def usuario_id(self) -> PydanticObjectId | None:
        u = getattr(self, "usuario", None)
        if u is None:
            return None
        if hasattr(u, "id"):
            return u.id
        if isinstance(u, PydanticObjectId):
            return u
        return None

    @property
    def livro_id(self) -> PydanticObjectId | None:
        l = getattr(self, "livro", None)
        if l is None:
            return None
        if hasattr(l, "id"):
            return l.id
        if isinstance(l, PydanticObjectId):
            return l
        return None


class CompraCreate(BaseModel):
    usuario_id: PydanticObjectId
    livro_id: PydanticObjectId
    quantidade: int = Field(..., gt=0)


class CompraUpdate(BaseModel):
    quantidade: int | None = Field(None, gt=0)


class CompraRead(BaseModel):
    id: PydanticObjectId | None = None
    usuario: Usuario | None = None
    livro: LivroRead | None = None
    quantidade: int | None = None
    preco_total: float | None = None

    model_config = {
        "from_attributes": True,
    }