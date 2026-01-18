from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, EmailStr


class AdminCreate(BaseModel):
    """
    Schema utilizado para criação de um administrador.

    Usado nos endpoints de criação.
    """
    nome: str = Field(..., min_length=1, description="Nome do administrador")
    email: EmailStr


class AdminUpdate(BaseModel):
    """
    Schema utilizado para atualização de dados do administrador.

    Todos os campos são opcionais.
    """
    nome: str | None = Field(None, min_length=1, description="Nome do administrador")
    email: EmailStr | None = None


class AdminBasic(BaseModel):
    """
    Schema básico de leitura do administrador.

    Usado normalmente quando o Admin é retornado
    como parte de outro recurso (ex: Livro).
    """
    id: PydanticObjectId
    nome: str | None = None
    email: str | None = None

    model_config = {
        "from_attributes": True
    }


class Admin(Document):
    """
    Documento que representa um administrador do sistema.

    O Admin é responsável por operações administrativas,
    como cadastro de livros.
    """
    nome: str | None = None
    email: str | None = None

    class Settings:
        """
        Configuração da coleção MongoDB.
        """
        name = "admin"
