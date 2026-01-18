from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field
from models.usuario import Usuario
from models.livro import Livro, LivroRead


class Compras(Document):
    """
    Documento que representa uma compra realizada por um usuário.

    Cada compra possui:
    - Um usuário associado
    - Um livro comprado
    - Quantidade adquirida
    - Preço total calculado no momento da compra
    """
    usuario: Link[Usuario]
    livro: Link[Livro]
    quantidade: int = 1
    preco_total: float | None = None

    class Settings:
        """
        Configuração da coleção MongoDB.
        """
        name = "compras"




class CompraCreate(BaseModel):
    """
    Schema utilizado para criação de uma nova compra.

    Recebe apenas os IDs do usuário e do livro,
    além da quantidade comprada.
    """
    usuario_id: PydanticObjectId
    livro_id: PydanticObjectId
    quantidade: int = Field(..., gt=0, description="Quantidade de livros comprados")


class CompraUpdate(BaseModel):
    """
    Schema utilizado para atualização de uma compra.

    Atualmente permite apenas a atualização da quantidade.
    """
    quantidade: int | None = Field(None, gt=0, description="Nova quantidade comprada")


class CompraRead(BaseModel):
    """
    Schema de leitura de compra.

    Retornado nos endpoints da API, contendo:
    - Usuário completo
    - Livro em formato de leitura (`LivroRead`)
    """
    id: PydanticObjectId | None = None
    usuario: Usuario | None = None
    livro: LivroRead | None = None
    quantidade: int | None = None
    preco_total: float | None = None

    model_config = {
        "from_attributes": True,
    }
