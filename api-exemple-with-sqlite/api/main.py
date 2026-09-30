from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import criar_db_tabelas

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a API...")
    print("Criando tabelas no banco de dados...")
    criar_db_tabelas()
    yield


app = FastAPI(title="API de Livros", description="API para gerenciar livros", version="1.0.0", lifespan=lifespan)