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
