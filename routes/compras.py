from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from models.compras import Compras
from fastapi import APIRouter


router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)

@router.get("/", response_model=Page[Compras])
async def get_compras() -> Page[Compras]:
    compras_page = await apaginate(Compras.find_all())
    if not compras_page.items:
        raise HTTPException(status_code=404, detail="Nenhuma compra encontrada")
    return compras_page

@router.post("/", response_model=Compras)
async def create_compra(compra: Compras) -> Compras:
    await compra.insert()
    return compra