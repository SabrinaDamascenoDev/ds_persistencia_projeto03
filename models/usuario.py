from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel


class Usuario(Document):
    """
    Documento que representa um usuário no banco de dados MongoDB.

    Esta classe é persistida automaticamente pelo Beanie e
    mapeada para a coleção `usuario`.
    """
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None

    class Settings:
        """
        Configurações específicas do documento Beanie.
        """
        name = "usuario"


class UsuarioCreate(BaseModel):
    """
    Schema utilizado para criação de um novo usuário.

    Não possui o campo `id`, pois este é gerado automaticamente
    pelo MongoDB.
    """
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None


class UsuarioRead(BaseModel):
    """
    Schema de leitura de usuário.

    Utilizado nas respostas da API, incluindo o campo `id`
    do documento persistido.
    """
    id: PydanticObjectId
    nome: str | None = None
    email: str | None = None
    endereco: str | None = None
    telefone: str | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
