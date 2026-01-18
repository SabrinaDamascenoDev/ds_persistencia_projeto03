from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from models.livro import Livro, LivroCreate, LivroRead, LivroUpdate
from models.admin import Admin

router = APIRouter(
    prefix="/livros",
    tags=["Livros"]
)

@router.get("/", response_model=Page[LivroRead])
async def get_livros(genero: str | None = Query(None)):
    """
    Lista livros com paginação e filtro opcional por gênero.
    Resolve explicitamente links (fetch_link) antes de converter para o schema de leitura.
    """
    query = Livro.find_all()

    if genero:
        query = query.find(Livro.genero == genero)

    async def transformer(livros):
        out = []
        for livro in livros:
            # resolve o link do admin para garantir que Livro.admin seja o documento Admin
            try:
                await livro.fetch_link("admin")
            except Exception:
                # se não conseguir resolver, mantemos o estado atual (será tratado pelo schema)
                pass
            # LivroRead usa from_attributes e a propriedade Livro.admin_id
            out.append(LivroRead.model_validate(livro))
        return out

    return await paginate(query, transformer=transformer)


@router.get("/{livro_id}", response_model=LivroRead)
async def get_livro(livro_id: PydanticObjectId):
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    await livro.fetch_link("admin")
    return LivroRead.model_validate(livro)

@router.post("/", response_model=LivroRead, status_code=201)
async def create_livro(livro_input: LivroCreate):
    admin = await Admin.get(livro_input.admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")

    livro = Livro(
        **livro_input.model_dump(exclude={"admin_id"}),
        admin=admin
    )
    await livro.insert()
    await livro.fetch_link("admin")
    return LivroRead.model_validate(livro)

@router.put("/{livro_id}", response_model=LivroRead)
async def update_livro(livro_id: PydanticObjectId, livro_in: LivroUpdate):
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    await livro.set(livro_in.model_dump(exclude_unset=True))
    await livro.fetch_link("admin")
    return LivroRead.model_validate(livro)

@router.delete("/{livro_id}", status_code=204)
async def delete_livro(livro_id: PydanticObjectId):
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    from models.compras import Compras
    await Compras.find(Compras.livro.id == livro_id).delete()
    await livro.delete()
    return None
