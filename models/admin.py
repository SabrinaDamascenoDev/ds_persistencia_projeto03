from beanie import Document, Link
from pydantic import BaseModel, ConfigDict

class AdminCreate(BaseModel):
    nome: str | None = None
    email: str | None = None

class AdminUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None

    
class Admin(Document):
    nome: str | None = None
    email: str | None = None

    class Settings:
        name = "admin"
