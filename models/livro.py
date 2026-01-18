from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel
from models.admin import Admin, AdminBasic


class LivroCreate(BaseModel):
    """
    Schema utilizado para criação de um livro.

    O campo `admin_id` representa o administrador responsável
    pelo cadastro do livro e será convertido para um Link[Admin]
    no momento da persistência.
    """
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    admin_id: PydanticObjectId


class LivroUpdate(BaseModel):
    """
    Schema utilizado para atualização parcial de um livro.

    Apenas os campos enviados serão atualizados.
    """
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None


class Livro(Document):
    """
    Documento que representa um livro no banco de dados MongoDB.

    Possui um relacionamento com o administrador responsável
    pelo cadastro do livro.
    """
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None

    admin: Link[Admin]

    class Settings:
        """
        Configurações específicas do documento Beanie.
        """
        name = "livro"

    @property
    def admin_id(self) -> PydanticObjectId | None:
        """
        Retorna o ID do administrador associado ao livro.

        - Se o link já foi resolvido (`fetch_link`), retorna `admin.id`
        - Se o campo ainda for apenas um ObjectId, retorna diretamente
        - Caso não exista, retorna None

        Essa propriedade facilita a interoperabilidade entre
        Document e schemas Pydantic.
        """
        admin = getattr(self, "admin", None)
        if admin is None:
            return None
        if hasattr(admin, "id"):
            return admin.id
        if isinstance(admin, (PydanticObjectId, str)):
            return admin
        return None


class LivroRead(BaseModel):
    """
    Schema de leitura de livro.

    Utilizado nas respostas da API, incluindo o administrador
    de forma resumida (`AdminBasic`).
    """
    id: PydanticObjectId | None = None
    titulo: str | None = None
    autor: str | None = None
    quantidade_paginas: int | None = None
    editora: str | None = None
    genero: str | None = None
    quantidade_estoque: int | None = None
    preco_uni: float | None = None
    admin: AdminBasic | None = None

    model_config = {
        "from_attributes": True,
    }
