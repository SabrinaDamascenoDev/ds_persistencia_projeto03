import asyncio
from database import init_db
from models.livro import Livro
# Se você tiver compras associadas a livros, é bom limpar também para evitar erro lá
from models.compras import Compras 

async def limpar_livros():
    print("🔄 Conectando ao banco de dados...")
    await init_db()


    print("🗑️ Removendo TODOS os Livros...")
    await Compras.delete_all()
    
    print("✅ Sucesso! A coleção de livros (e compras) está vazia.")

if __name__ == "__main__":
    asyncio.run(limpar_livros())