from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page, paginate
from models.livro import Livro, LivroCreate, LivroRead, LivroUpdate
from models.admin import Admin
from models.compras import Compras


router = APIRouter(
    prefix="/livros",
    tags=["Livros"]
)

@router.get("/", response_model=Page[Livro])
async def get_livros(
    genero: str | None = Query(None),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
):
    """
    Lista livros com paginação manual (skip/limit).
    """
    
    query = Livro.find_all(fetch_links=True)

    if genero:
        query = query.find(Livro.genero == genero)

    total = await query.count()
    skip = (page - 1) * size

    livros_encontrados = await query.skip(skip).limit(size).to_list()

    return {
        "items": [Livro.model_validate(livro) for livro in livros_encontrados],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }


@router.get("/{livro_id}", response_model=LivroRead)
async def get_livro(livro_id: PydanticObjectId):
    """
    Retorna os dados de um livro específico pelo ID.
    """
    livro = await Livro.get(livro_id, fetch_links=True)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return LivroRead.model_validate(livro)



@router.post("/", response_model=LivroRead, status_code=201)
async def create_livro(livro_input: LivroCreate):
    """
    Cria um novo livro.

    O admin responsável é validado antes da criação
    e associado ao livro via referência (Link).
    """
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
    """
    Atualiza os dados de um livro existente.

    Apenas os campos enviados na requisição são modificados.
    """
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    await livro.set(livro_in.model_dump(exclude_unset=True))
    await livro.fetch_link("admin")

    return LivroRead.model_validate(livro)


@router.delete("/{livro_id}", status_code=204)
async def delete_livro(livro_id: PydanticObjectId):
    """
    Remove um livro pelo ID.

    Antes da exclusão do livro, todas as compras associadas
    a ele são removidas para manter a integridade dos dados.
    """
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    await Compras.find(Compras.livro.id == livro_id).delete()

    await livro.delete()
    return None
