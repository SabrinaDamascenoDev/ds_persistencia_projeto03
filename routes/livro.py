from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page, paginate
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

    Os dados do admin responsável pelo livro são resolvidos manualmente
    utilizando `fetch_link`, pois o retorno é convertido para um schema
    de leitura (`LivroRead`).
    """
    query = Livro.find_all()

    if genero:
        query = query.find(Livro.genero == genero)

    livros = await query.to_list()

    for livro in livros:
        await livro.fetch_link("admin")

    livros_read = [LivroRead.model_validate(livro) for livro in livros]

    return paginate(livros_read)


@router.get("/{livro_id}", response_model=LivroRead)
async def get_livro(livro_id: PydanticObjectId):
    """
    Retorna os dados de um livro específico pelo ID.
    """
    livro = await Livro.get(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    await livro.fetch_link("admin")
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

    from models.compras import Compras

    await Compras.find(Compras.livro.id == livro_id).delete()

    await livro.delete()
    return None
