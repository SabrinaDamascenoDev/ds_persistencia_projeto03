from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import usuario, admin, livro, compras
from database import init_db, close_db
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
 

app.include_router(usuario.router)
app.include_router(admin.router)
app.include_router(livro.router)
app.include_router(compras.router)
add_pagination(app)