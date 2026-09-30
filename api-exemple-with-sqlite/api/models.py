from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class LivroBase(SQLModel):
    autor: str = Field(index=True)
    titulo: str = Field(index=True)
    editora: str = Field(index=True)
    ano: int = Field(index=True)

class Livro(LivroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, index=True, unique=True)

class LivroResposta(LivroBase):
    uuid: UUID

class LivroPost(LivroBase):
    pass

class LivroPut(LivroBase):
    pass

class LivroPatch(SQLModel):
    autor: str | None = None
    titulo: str | None = None
    editora: str | None = None
    ano: int | None = None

class ConfirmaDelete(BaseModel):
    mensagem: str
    uuid: UUID