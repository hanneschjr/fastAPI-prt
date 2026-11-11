from sqlmodel import create_engine, SQLModel, Session, select
from pathlib import Path
from api.models import Livro # importação necessária para que o módlulo models.py seja executado e que Livro seja registrado no SQLModel.metadata
from uuid import UUID

DATABASE_PATH = Path(__file__).parent / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False}  # Necessário para SQLite


# Carga de dados inicial (livros)

engine = create_engine(DATABASE_URL, echo=True, connect_args=CONNECT_ARGS)


# Executa a criação das tabelas que estão definidas no SQLModel.metadata, que inclui a tabela Livro definida no models.py
def criar_db_tabelas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

