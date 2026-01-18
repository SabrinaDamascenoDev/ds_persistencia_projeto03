import asyncio
from database import init_db
from models.livro import Livro

async def limpar_livros():
    await init_db()
    await Livro.delete_all()
    print("Coleção de livros limpa!")

if __name__ == "__main__":
    asyncio.run(limpar_livros())