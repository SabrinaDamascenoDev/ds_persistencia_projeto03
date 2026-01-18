from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.livro import Livro, LivroCreate, LivroRead, LivroUpdate
from models.admin import Admin

router = APIRouter(
    prefix="/livros",
    tags=["Livros"]
)

@router.get("/", response_model=Page[Livro])
async def get_livros() -> Page[Livro]:
    return await apaginate(Livro.find_all())

@router.get("/{livro_id}", response_model=Livro)
async def get_livro(livro_id: PydanticObjectId) -> Livro:
    livro = await Livro.get(livro_id, fetch_links=True)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro

@router.post("/", response_model=LivroRead)
async def create_livro(livro_input: LivroCreate):
    admin = await Admin.get(livro_input.admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")

    livro = Livro(
        **livro_input.model_dump(exclude={"admin_id"}),
        admin=admin
    )
    await livro.insert()

    return LivroRead(
        id=livro.id,
        titulo=livro.titulo,
        autor=livro.autor,
        quantidade_paginas=livro.quantidade_paginas,
        editora=livro.editora,
        genero=livro.genero,
        quantidade_estoque=livro.quantidade_estoque,
        preco_uni=livro.preco_uni,
        admin_id=admin.id
    )
