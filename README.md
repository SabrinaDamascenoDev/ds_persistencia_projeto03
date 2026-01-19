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




