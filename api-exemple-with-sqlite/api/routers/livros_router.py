from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from api.models import ConfirmaDelete, Livro, LivroPatch, LivroPut, LivroResposta, LivroPost
from typing import Annotated
from sqlmodel import Session, func, select
from api.database import get_session

router = APIRouter(prefix="/livros", tags=["livros"])


# SessionDep é um apelido para o tipo Session que é injetado como dependência usando Depends(get_session).
# Isso permite que as rotas do FastAPI recebam automaticamente uma sessão de banco de dados quando forem chamadas.
SessionDep = Annotated[Session, Depends(get_session)] 

# # GET - Listar Livros - sem paginação
# @router.get("/", response_model=list[LivroResposta])
# async def listar_livros(session: SessionDep) -> list[LivroResposta]:
#     livros = session.exec(select(Livro)).all()
#     return [LivroResposta.model_validate(livro) for livro in livros] # é redundnate! Poderia ser "return livros"


# GET - Listar Livros - com paginação
@router.get("/", response_model=list[LivroResposta])
async def listar_livros(session: SessionDep, response: Response, page: int= Query(1, ge=1)) -> list[LivroResposta]:
    PAGE_SIZE = 10
    total_items = session.exec(select(func.count()).select_from(Livro)).one()
    total_pages = (total_items + PAGE_SIZE - 1) // PAGE_SIZE  # Calcula o número total de páginas

    if page > total_pages and total_pages > 0:
        page = total_pages  # Ajusta para a última página se a página solicitada for maior que o total de páginas
        
    offset = (page - 1) * PAGE_SIZE
    query = (select(Livro).order_by(Livro.id).limit(PAGE_SIZE).offset(offset))
    livros = session.exec(query).all()
    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total_items)
    return [LivroResposta.model_validate(livro) for livro in livros]  # Retorna a página pedida 
    
    
# GET - Obter um livro
@router.get("/{livro_id}", response_model=LivroResposta,
            responses={404:{"description": "Livro não encontrado!"}}) # responses aqui só na documentação da API.
async def obter_livro(livro_id: UUID, session:SessionDep) -> LivroResposta:
    if livro := session.exec(select(Livro).where(Livro.uuid == livro_id)).first():
        return LivroResposta.model_validate(livro)
    raise HTTPException(status_code=404, detail="Livro não encontrado!")

# POST - Adicionar um livro
@router.post("/", response_model=LivroResposta, status_code=201) 
async def adicionar_livro(livro: LivroPost, session:SessionDep) -> LivroResposta:
    livro_gravado = Livro(**livro.model_dump()) 
    session.add(livro_gravado)
    session.commit()
    return LivroResposta.model_validate(livro_gravado)

# PUT - Mudar todos os campos de um livro
@router.put("/{livro_id}", response_model=LivroResposta,
             responses={404: {"description": "Livro não encontrado!"}}) # responses aqui só na documentação.
async def atualizar_livro(livro_id:UUID, livro_update:LivroPut, session:SessionDep) -> LivroResposta:
    if livro := session.exec(select(Livro).where(Livro.uuid == livro_id)).first():
        for key, value in livro_update: # pega os campos nomeados do modelo
            setattr(livro, key, value) # altera o objeto livro na memória do Python (antes de ir ao banco)
        session.add(livro) # desnecessário pois o objeto livro já exite na sessão e não precisa ser substituído
        session.commit()
        session.refresh(livro) # retorna o livro que está na base de dados só para ter certeza do que foi.
        return LivroResposta.model_validate(livro)

    raise HTTPException(status_code=404, detail="Livro não encontrado!")

# PATCH - Mudar campos selecionados de um livro
@router.patch("/{livro_id}", response_model=LivroResposta,
             responses={404: {"description": "Livro não encontrado!"},
                        400: {"description":"Nenhum dado enviado para atualização!"}}) # responses aqui só na documentação.
async def atualizar_parcial_livro(livro_id:UUID, livro_update:LivroPatch, session:SessionDep) -> LivroResposta:
    update_data = livro_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado para atualização!")

    if livro := session.exec(select(Livro).where(Livro.uuid == livro_id)).first():
        for key, value in update_data.items(): # pega os campos nomeados do dicionário update_data
            setattr(livro, key, value) # altera o objeto livro na memória do Python (antes de ir ao banco)
        session.add(livro) # desnecessário pois o objeto livro já exite na sessão e não precisa ser substituído
        session.commit()
        session.refresh(livro) # retorna o livro que está na base de dados só para ter certeza do que foi.
        return LivroResposta.model_validate(livro)

    raise HTTPException(status_code=404, detail="Livro não encontrado!")


# DELETE - Deletar um livro
@router.delete("/{livro_id}", response_model=ConfirmaDelete,
             responses={404: {"description": "Livro não encontrado!"}}) # responses aqui só na documentação.
async def deletar_livro(livro_id:UUID, session:SessionDep) -> ConfirmaDelete:
    if livro := session.exec(select(Livro).where(Livro.uuid == livro_id)).first():
        titulo = livro.titulo
        session.delete(livro)
        session.commit()
        return ConfirmaDelete(mensagem=f"Livro '{titulo}' deletado com sucesso!", uuid=livro_id)
    
    raise HTTPException(status_code=404, detail="Livro não encontrado!")


