from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.beanie import apaginate
from models.compras import Compras, ComprasCreate
from models.livro import Livro
from models.usuario import Usuario

router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)

@router.get("/", response_model=Page[Compras])
async def get_compras():
    return await apaginate(Compras.find_all(), fetch_links=True)

@router.post("/", response_model=Compras)
async def create_compra(compra_in: ComprasCreate):
    usuario = await Usuario.get(compra_in.usuario)
    livro = await Livro.get(compra_in.livro)


    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    nova_compra = Compras(
        usuario=usuario,
        livro=livro,
        quantidade_comprados=compra_in.quantidade_comprados,
        preco_pago=compra_in.preco_pago,
        data_compra=compra_in.data_compra
    )

    await nova_compra.insert()
    return nova_compra

@router.delete("/{compra_id}", status_code=204)
async def delete_compra(compra_id: PydanticObjectId):
    compra = await Compras.get(compra_id)

    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    await compra.delete()
    
    return None