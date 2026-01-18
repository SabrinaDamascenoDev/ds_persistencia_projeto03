import asyncio
import random
from database import init_db
from models.usuario import Usuario
from models.admin import Admin
from models.livro import Livro
from models.compras import Compras

async def populate():
    print("🔄 Conectando ao banco de dados...")
    await init_db()

    print("🗑️  APAGANDO TUDO (Limpando o banco)...")

    await Compras.delete_all()
    await Livro.delete_all()
    await Admin.delete_all()
    await Usuario.delete_all()
    print("✨ Banco limpo!")

    print("👤 Criando Admins...")
    admins = []

    for i in range(1, 6):
        adm = Admin(nome=f"Admin {i}", email=f"admin{i}@livraria.com")
        admin_salvo = await adm.insert() 
        admins.append(admin_salvo)

    print("📚 Criando Livros...")
    livros = []
    for i in range(1, 21):
        dono = random.choice(admins)
        
        livro = Livro(
            titulo=f"Livro Exemplo {i}",
            autor=f"Autor {i}",
            quantidade_paginas=100 + i*10,
            editora=f"Editora {random.randint(1, 5)}",
            genero=random.choice(["Tecnologia", "Fantasia", "Romance", "Aventura"]),
            quantidade_estoque=random.randint(5, 50),
            preco_uni=round(random.uniform(20.0, 100.0), 2),
            admin=dono 
        )
        livro_salvo = await livro.insert()
        livros.append(livro_salvo)

    print("🧑 Criando Usuários...")
    usuarios = []

    for i in range(1, 11):
        user = Usuario(
            nome=f"Usuario {i}", 
            email=f"user{i}@gmail.com",
            endereco=f"Rua Teste, {i}",
            telefone=f"1199999{i:04d}"
        )
        user_salvo = await user.insert()
        usuarios.append(user_salvo)

    print("🛒 Criando Compras...")
 
    for i in range(30):
        comprador = random.choice(usuarios)
        livro_escolhido = random.choice(livros)
        qtd = random.randint(1, 3)
        total = round(livro_escolhido.preco_uni * qtd, 2)
        
        compra = Compras(
            usuario=comprador, 
            livro=livro_escolhido, 
            quantidade=qtd,
            preco_total=total
        )
        await compra.insert()

    print("✅ Banco de dados populado com SUCESSO! (Dados antigos removidos)")

if __name__ == "__main__":
    asyncio.run(populate())