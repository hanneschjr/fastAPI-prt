from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 1. Inicialização da API
app = FastAPI(title="API de Livros", description="API para gerenciar livros", version="1.0.0")


# 2. Base de dados em memória (dicionário)
livros_db = {
    1: {"uuid": uuid4(), "autor": "George Orwell", "titulo": "1984", "editora": "Companhia das Letras","ano": 1949},
    2: {"uuid": uuid4(), "autor": "J.R.R. Tolkien", "titulo": "O Hobbit", "editora": "HarperCollins","ano": 1937},
}

# 3. Definição do modelo de dados
class Livro(BaseModel):
    uuid: UUID
    autor: str
    titulo: str
    editora: str
    ano: int

class LivroPostPut(BaseModel):
    autor: str
    titulo: str
    editora: str
    ano: int

class LivroPatch(BaseModel):
    autor: str | None = None
    titulo: str | None = None
    editora: str | None = None
    ano: int | None = None

# 4. Implementando o endpoint de leitura (GET)
@app.get("/livros", response_model=List[Livro])
async def listar_livros() -> List[Livro]:
    return [Livro(**livro) for livro in livros_db.values()]     

# 5. Implementando o endpoint de exibir um livro pelo uuid (GET)
@app.get("/livros/{livro_id}", response_model=Livro)
async def exibir_livro_por_id(livro_id: UUID) -> Livro:
    for livro in livros_db.values():
        if livro["uuid"] == livro_id:
            return Livro(**livro) # type: ignore
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# 6. Implementando o endpoint de criação de livro (POST)
@app.post("/livros", response_model=Livro, status_code=200)
async def adicionar_livro(livro: LivroPostPut)-> Livro:
    novo_uuid = uuid4()
    novo_id = max(livros_db.keys()) + 1 if livros_db else 1
    livro_gravado = Livro(uuid=novo_uuid, autor=livro.autor, titulo=livro.titulo, editora=livro.editora, ano=livro.ano)
    livros_db[novo_id] = livro_gravado.model_dump()
    return livro_gravado

# 7. Implementando o endpoint de atualização de livro (PUT)
@app.put("/livros/{livro_id}", response_model=Livro)    
async def atualizar_livro(livro_id: UUID, livro_update: LivroPostPut) -> Livro:
    for id, livro_existente in livros_db.items():
        if livro_existente["uuid"] == livro_id:
            livros_db[id] = dict(uuid=livro_id, **livro_update.model_dump()) # model_dump() retorna um dicionário com os dados do modelo)
            return Livro(**livros_db[id]) # type: ignore
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# 8. Implementando o endpoint de atualização parcial de livro (PATCH)
@app.patch("/livros/{livro_id}", response_model=Livro)
async def atualizar_parcial_livro(livro_id: UUID, livro_update: LivroPatch) -> Livro:
    for id, livro_existente in livros_db.items():
        if livro_existente["uuid"] == livro_id:
            livro_atualizado = {**livro_existente, **livro_update.model_dump()}
            livros_db[id] = livro_atualizado
            return Livro(**livros_db[id]) # type: ignore
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# if __name__ == "__main__":
#     print(livros_db.values())
#     print('#######################')
#     print([Livro(**livro) for livro in livros_db.values()])       