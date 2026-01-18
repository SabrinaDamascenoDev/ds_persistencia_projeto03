from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.beanie import apaginate

from models.compras import Compras, CompraCreate, CompraRead, CompraUpdate
from models.usuario import Usuario
from models.livro import Livro


router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)

from fastapi import APIRouter, HTTPException, Query
from beanie.odm.fields import PydanticObjectId
from typing import List
from models.compras import Compras, CompraCreate, CompraRead, CompraUpdate
from models.usuario import Usuario
from models.livro import Livro

router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


@router.get("/", response_model=Page[Compras])
async def get_compras(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """
    Lista compras com paginação.

    Os relacionamentos (`usuario` e `livro`) são resolvidos automaticamente
    com `fetch_links=True`.
    """
    skip = (page - 1) * size

    compras = await Compras.find_all(fetch_links=True).skip(skip).limit(size).to_list()

    total = await Compras.count()

    return {
        "items": [Compras.model_validate(c) for c in compras], 
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }


@router.get("/{compra_id}", response_model=CompraRead)
async def get_compra(compra_id: PydanticObjectId):
    """
    Retorna os dados de uma compra específica pelo ID.

    Resolve os relacionamentos de usuário e livro antes da resposta.
    """
    compra = await Compras.get(compra_id, fetch_links=True)
    return CompraRead.model_validate(compra)


@router.post("/", response_model=CompraRead, status_code=201)
async def create_compra(compra_in: CompraCreate):
    """
    Cria uma nova compra.

    Regras de negócio:
    - O usuário deve existir
    - O livro deve existir
    - Deve haver estoque suficiente
    - O estoque do livro é decrementado após a compra
    - O preço total é calculado com base no preço unitário do livro
    """
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

    new_q = (livro.quantidade_estoque or 0) - compra_in.quantidade
    await livro.set({"quantidade_estoque": new_q})

    await compra.fetch_link("usuario")
    await compra.fetch_link("livro")
    await compra.livro.fetch_link("admin") 

    return CompraRead.model_validate(compra)


@router.put("/{compra_id}", response_model=CompraRead)
async def update_compra(compra_id: PydanticObjectId, compra_in: CompraUpdate):
    """
    Atualiza a quantidade de uma compra existente.

    Ajusta o estoque do livro considerando a diferença entre a
    quantidade antiga e a nova.
    """
    compra = await Compras.get(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")

    if compra_in.quantidade is None:
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

    if delta > 0 and (livro.quantidade_estoque or 0) < delta:
        raise HTTPException(status_code=400, detail="Estoque insuficiente para aumentar quantidade")

    await livro.set({"quantidade_estoque": (livro.quantidade_estoque or 0) - delta})

    preco_unit = livro.preco_uni or 0.0
    preco_total = float(preco_unit) * new_q

    await compra.set({
        "quantidade": new_q,
        "preco_total": preco_total
    })

    await compra.fetch_link("usuario")
    await compra.fetch_link("livro")
    await compra.livro.fetch_link("admin")

    return CompraRead.model_validate(compra)


@router.delete("/{compra_id}", status_code=204)
async def delete_compra(compra_id: PydanticObjectId):
    """
    Remove uma compra.

    O estoque do livro é restaurado com a quantidade da compra removida.
    """
    compra = await Compras.get(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")

    await compra.fetch_link("livro")
    livro = compra.livro

    if livro:
        await livro.set({
            "quantidade_estoque": (livro.quantidade_estoque or 0) + (compra.quantidade or 0)
        })

    await compra.delete()
    return None


@router.get("/stats/total")
async def total_compras():
    """
    Retorna o número total de compras realizadas.

    Mede a quantidade de documentos na collection `compras`.
    """
    return {"total_compras": await Compras.count()}


@router.get("/stats/compras-por-livro")
async def compras_por_livro():
    """
    Retorna o total de compras por livro.

    Cada incremento representa uma compra realizada,
    independentemente da quantidade de itens.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$livro.$id",
                "total": {"$sum": 1}
            }
        }
    ]

    result = await Compras.aggregate(pipeline).to_list()

    return [
        {
            "livro_id": str(item["_id"]),
            "total": item["total"]
        }
        for item in result
    ]


@router.get("/stats/livros-mais-vendidos")
async def livros_mais_vendidos():
    """
    Retorna o ranking de livros mais vendidos.

    Soma a quantidade total de unidades vendidas por livro,
    ordenando do mais vendido para o menos vendido.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$livro.$id",
                "quantidade": {"$sum": "$quantidade"}
            }
        },
        {"$sort": {"quantidade": -1}}
    ]

    result = await Compras.aggregate(pipeline).to_list()

    return [
        {
            "livro_id": str(item["_id"]),
            "quantidade": item["quantidade"]
        }
        for item in result
    ]
