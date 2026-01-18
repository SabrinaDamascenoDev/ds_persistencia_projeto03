from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from models.compras import Compras, CompraCreate, CompraRead, CompraUpdate
from models.usuario import Usuario
from models.livro import Livro

router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


@router.get("/", response_model=Page[CompraRead])
async def get_compras(usuario_id: PydanticObjectId | None = Query(None),
                      livro_id: PydanticObjectId | None = Query(None)):
    """
    Lista compras com paginação e filtros opcionais por usuario_id e livro_id.
    Resolve links antes de converter para schema de leitura.
    """
    query = Compras.find_all()

    if usuario_id:
        query = query.find(Compras.usuario.id == usuario_id)
    if livro_id:
        query = query.find(Compras.livro.id == livro_id)

    async def transformer(items):
        out = []
        for c in items:
            # garante que links estejam resolvidos para from_attributes/propriedades funcionarem
            try:
                await c.fetch_link("usuario")
                await c.fetch_link("livro")
            except Exception:
                pass
            out.append(CompraRead.model_validate(c))
        return out

    return await paginate(query, transformer=transformer)


@router.get("/{compra_id}", response_model=CompraRead)
async def get_compra(compra_id: PydanticObjectId):
    compra = await Compras.get(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    await compra.fetch_link("usuario")
    await compra.fetch_link("livro")
    return CompraRead.model_validate(compra)


@router.post("/", response_model=CompraRead, status_code=201)
async def create_compra(compra_in: CompraCreate):
    usuario = await Usuario.get(compra_in.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    livro = await Livro.get(compra_in.livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if livro.quantidade_estoque is None or livro.quantidade_estoque < compra_in.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    preco_unit = livro.preco_uni or 0.0
    preco_total = float(preco_unit) * compra_in.quantidade

    compra = Compras(
        usuario=usuario,
        livro=livro,
        quantidade=compra_in.quantidade,
        preco_total=preco_total
    )
    await compra.insert()

    # atualiza estoque do livro
    new_q = (livro.quantidade_estoque or 0) - compra_in.quantidade
    await livro.set({"quantidade_estoque": new_q})

    await compra.fetch_link("usuario")
    await compra.fetch_link("livro")
    return CompraRead.model_validate(compra)


@router.put("/{compra_id}", response_model=CompraRead)
async def update_compra(compra_id: PydanticObjectId, compra_in: CompraUpdate):
    compra = await Compras.get(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")

    # só permitimos ajuste de quantidade aqui, ajustando o estoque do livro também
    if compra_in.quantidade is None:
        # nada para fazer
        await compra.fetch_link("usuario")
        await compra.fetch_link("livro")
        return CompraRead.model_validate(compra)

    await compra.fetch_link("livro")
    livro = compra.livro
    if not livro:
        raise HTTPException(status_code=500, detail="Livro referenciado ausente")

    old_q = compra.quantidade or 0
    new_q = compra_in.quantidade
    delta = new_q - old_q

    # se delta > 0 -> diminuir estoque; delta < 0 -> aumentar estoque
    if delta > 0:
        if (livro.quantidade_estoque or 0) < delta:
            raise HTTPException(status_code=400, detail="Estoque insuficiente para aumentar quantidade")
    # aplica mudança no estoque
    await livro.set({"quantidade_estoque": (livro.quantidade_estoque or 0) - delta})

    # atualiza campos da compra (quantidade e preco_total)
    preco_unit = livro.preco_uni or 0.0
    preco_total = float(preco_unit) * new_q
    await compra.set({"quantidade": new_q, "preco_total": preco_total})

    await compra.fetch_link("usuario")
    await compra.fetch_link("livro")
    return CompraRead.model_validate(compra)


@router.delete("/{compra_id}", status_code=204)
async def delete_compra(compra_id: PydanticObjectId):
    compra = await Compras.get(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")

    # restaurar estoque do livro antes de apagar
    await compra.fetch_link("livro")
    livro = compra.livro
    if livro:
        await livro.set({"quantidade_estoque": (livro.quantidade_estoque or 0) + (compra.quantidade or 0)})

    await compra.delete()
    return None