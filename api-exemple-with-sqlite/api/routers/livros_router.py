from fastapi import APIRouter, Depends
from api.models import Livro, LivroResposta
from typing import Annotated
from sqlmodel import Session, select
from api.database import get_session

router = APIRouter(prefix="/livros", tags=["livros"])


# SessionDep é um apelido para o tipo Session que é injetado como dependência usando Depends(get_session).
# Isso permite que as rotas do FastAPI recebam automaticamente uma sessão de banco de dados quando forem chamadas.
SessionDep = Annotated[Session, Depends(get_session)] 

# GET - Listar Livros
@router.get("/", response_model=list[LivroResposta])
async def listar_livros(session: SessionDep) -> list[LivroResposta]:
    livros = session.exec(select(Livro)).all()
    return [LivroResposta.model_validate(livro) for livro in livros]