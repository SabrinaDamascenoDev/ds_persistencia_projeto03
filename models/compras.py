from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import Field
from pydantic import BaseModel
from models.livro import Livro
from models.usuario import Usuario
from datetime import datetime

class Compras(Document):
    usuario: Link[Usuario]
    livro: Link[Livro]
    quantidade_comprados: int = Field(gt=0)
    preco_pago: float
    data_compra: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "compras"

class ComprasCreate(BaseModel):
    usuario: PydanticObjectId = Field(..., description="ID do Usuário")
    livro: PydanticObjectId = Field(..., description="ID do Livro")
    quantidade_comprados: int = Field(gt=0)
    preco_pago: float
    data_compra: datetime = Field(default_factory=datetime.utcnow)

class ComprasUpdate(BaseModel):
    usuario: PydanticObjectId = Field(..., description="ID do Usuário")
    livro: PydanticObjectId = Field(..., description="ID do Livro")
    quantidade_comprados: int = Field(gt=0)
    preco_pago: float