from beanie import Document, Link
from pydantic import BaseModel, Field, EmailStr

class AdminCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr

class AdminUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1)
    email: EmailStr | None = None

    
class Admin(Document):
    nome: str | None = None
    # manter o campo como str no Document evita falhas ao ler dados antigos inválidos.
    # A validação de formato de email fica restrita aos schemas de entrada (AdminCreate/AdminUpdate).
    email: str | None = None

    class Settings:
        name = "admin"
