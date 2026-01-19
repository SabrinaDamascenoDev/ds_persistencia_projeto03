## 📊 Diagrama de Classes

```mermaid
classDiagram
    class Usuario {
        +PydanticObjectId id
        +String nome
        +String email
        +String endereco
        +String telefone
    }

    class Admin {
        +PydanticObjectId id
        +String nome
        +String email
    }

    class Livro {
        +PydanticObjectId id
        +String titulo
        +String autor
        +Integer quantidade_paginas
        +String editora
        +String genero
        +Integer quantidade_estoque
        +Float preco_uni
        +Link~Admin~ admin
    }

    class Compras {
        +PydanticObjectId id
        +Link~Usuario~ usuario
        +Link~Livro~ livro
        +Integer quantidade
        +Float preco_total
    }

    Admin "1" --o "*" Livro : cadastra
    Usuario "1" --o "*" Compras : realiza
    Livro "1" --o "*" Compras : contido em




# 📦 ds-persistencia-projeto03

Projeto backend desenvolvido com **FastAPI**, **Beanie (ODM)** e **MongoDB**, utilizando **uv** para gerenciamento de dependências e ambiente virtual.

---

## 🚀 Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- Beanie
- MongoDB
- fastapi-pagination
- python-dotenv
- uv

---

## 📁 Estrutura do Projeto

```text
.
├── main.py
├── database.py
├── models/
│   └── livro.py
├── routes/
│   └── livros.py
├── .env
├── pyproject.toml
├── docker-compose.yaml
├── .python-version
├── uv.lock
└── README.md
```
Como instalar o uv

Caso não tenha o uv instalado, execute:


# MacOS / Linux
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
# Windows (PowerShell)
```bash
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```



# ⚙️ Instalação e Configuração
1. Clone o repositório
```bash
git clone https://github.com/SabrinaDamascenoDev/ds_persistencia_projeto03
cd ds-persistencia-projeto03
```

# 2. Crie o Ambiente Virtual

Gere a pasta .venv usando o comando:
```bash
uv venv --python 3.12
```

# 3. Ative o Ambiente Virtual

Antes de instalar as dependências, ative o ambiente:

Windows (PowerShell):
```bash
.venv\Scripts\activate
```
Linux / macOS:
```bash
source .venv/bin/activate
```
# 4. Instale as dependências

O uv criará o ambiente virtual e baixará as bibliotecas automaticamente:

```bash
uv sync
```
# ▶️ Como Rodar

Para iniciar o servidor de desenvolvimento:

```bash
fastapi run main.py
```
O servidor estará rodando em: https://www.google.com/search?q=http://127.0.0.1:8000