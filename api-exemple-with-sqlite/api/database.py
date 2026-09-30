from sqlmodel import create_engine, SQLModel, Session, select
from pathlib import Path

from api.models import Livro


DATABASE_PATH = Path(__file__).parent / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False}  # Necessário para SQLite

engine = create_engine(DATABASE_URL, echo=True, connect_args=CONNECT_ARGS)

def criar_db_tabelas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session