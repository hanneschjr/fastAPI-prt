from sqlmodel import create_engine, SQLModel, Session, select
from pathlib import Path
from api.models import Livro # importação necessária para que o módlulo models.py seja executado e que Livro seja registrado no SQLModel.metadata
from uuid import UUID

DATABASE_PATH = Path(__file__).parent / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False}  # Necessário para SQLite


# Carga de dados inicial (livros)
livros_default_data = [
    {"uuid": UUID("89b73751-0a54-4377-a380-3a4baedba58d"), "autor": "George Orwell", "titulo": "1984", "editora": "Companhia das Letras","ano": 1949},
    {"uuid": UUID("addf905d-e737-430a-bdcf-069b5169cd9c"), "autor": "J.R.R. Tolkien", "titulo": "O Hobbit", "editora": "HarperCollins","ano": 1937},
]

engine = create_engine(DATABASE_URL, echo=True, connect_args=CONNECT_ARGS)

# Executa a criação das tabelas que estão definidas no SQLModel.metadata, que inclui a tabela Livro definida no models.py
def criar_db_tabelas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def adicionar_livros_default():
    with Session(engine) as session:
        if not session.exec(select(Livro)).first():  # Verifica se já existem livros no banco de dados
            for livro_data in livros_default_data:
                livro = Livro(**livro_data)
                session.add(livro)
            session.commit()
