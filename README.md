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

Como instalar o uv

Caso não tenha o uv instalado, execute:
Bash

# MacOS / Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell)
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

⚙️ Instalação e Configuração
1. Clone o repositório
Bash

git clone [https://github.com/seu-usuario/ds-persistencia-projeto03.git](https://github.com/seu-usuario/ds-persistencia-projeto03.git)
cd ds-persistencia-projeto03

2. Configure o ambiente (.env)

Crie um arquivo chamado .env na raiz do projeto e configure a conexão com o banco:
Snippet de código

MONGODB_URI="mongodb://localhost:27017"
DATABASE_NAME="ds_projeto03_db"

3. Instale as dependências

O uv criará o ambiente virtual e baixará as bibliotecas automaticamente:
Bash

uv sync

▶️ Como Rodar

Para iniciar o servidor de desenvolvimento:
Bash

uv run fastapi dev main.py

O servidor estará rodando em: https://www.google.com/search?q=http://127.0.0.1:8000