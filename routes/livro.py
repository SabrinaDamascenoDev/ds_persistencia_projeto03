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
    return await apaginate(Livro.find_all(), fetch_links=True)

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
        **livro.model_dump(),
        admin_id=admin.id
    )

@router.get("/{livro_id}", response_model=Livro)
async def get_livro(livro_id: PydanticObjectId):
    livro = await Livro.get(livro_id, fetch_links=True)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro

@router.delete("/{livro_id}", status_code=204)
async def delete_livro(livro_id: PydanticObjectId):
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    from models.compras import Compras
    await Compras.find(Compras.livro.id == livro_id).delete()

    await livro.delete()
    
    return None