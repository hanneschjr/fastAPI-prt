from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# 1. Inicialização da API
app = FastAPI(title="API de Livros", description="API para gerenciar livros", version="1.0.0")


# 2. Base de dados em memória (dicionário)
livros_db = {
    1: {"id": uuid4(), "autor": "George Orwell", "titulo": "1984", "editora": "Companhia das Letras","ano": 1949},
    2: {"id": uuid4(), "autor": "J.R.R. Tolkien", "titulo": "O Hobbit", "editora": "HarperCollins","ano": 1937},
}


# 3. Definição do modelo de dados
class Livro(BaseModel):
    id: UUID
    autor: str
    titulo: str
    editora: str
    ano: int

# 4. Implementando o endpoint de leitura (GET)
@app.get("/livros", response_model=List[Livro])
async def listar_livros() -> List[Livro]:
    return [Livro(**livro) for livro in livros_db.values()]     


# 5. Implementando o endpoint de exibir um livro pelo id (GET)
@app.get("/livros/{livro_id}", response_model=Livro)
async def exibir_livro(livro_id: int) -> Livro:
    if livro_id not in livros_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return Livro(**livros_db[livro_id])

# if __name__ == "__main__":
#     print(livros_db.values())
#     print('#######################')
#     print([Livro(**livro) for livro in livros_db.values()])       