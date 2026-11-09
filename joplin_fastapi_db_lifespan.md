# Estrutura para iniciar a base de dados no FastAPI com `lifespan`

Quando a aplicação FastAPI sobe, a função assíncrona `lifespan` é usada para executar ações de ciclo de vida da API.

A ideia principal é:

- Antes do `yield`: ações executadas na inicialização da aplicação.
- Depois do `yield`: ações executadas no encerramento da aplicação.

## Estrutura básica

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.database import criar_db_tabelas, adicionar_livros_default

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Antes do yield = startup / antes da API ficar disponível
    print("Iniciando a API...")
    print("Criando tabelas no banco de dados...")
    criar_db_tabelas()
    adicionar_livros_default()

    yield

    # Depois do yield = shutdown / quando a API está encerrando
    print("Encerrando a API...")
    # fechar conexões, liberar recursos, encerrar sessão do banco, etc.

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar livros",
    version="1.0.0",
    lifespan=lifespan,
)
```

## O que acontece em cada etapa

### Antes do `yield` (startup)

Estas ações são executadas quando a API inicia:

- `print("Iniciando a API...")` — registra o início do processo.
- `criar_db_tabelas()` — garante que as tabelas existam no banco.
- `adicionar_livros_default()` — insere dados iniciais, caso sejam necessários.

É o momento ideal para:

- criar o esquema do banco;
- preencher dados padrão;
- abrir conexões ou inicializar pools;
- preparar recursos que a aplicação vai usar.

### `yield`

O `yield` marca o ponto em que a API já foi inicializada e fica pronta para receber requisições.

A partir daqui, a aplicação continua em execução normalmente.

### Depois do `yield` (shutdown)

Depois que a aplicação deixa de rodar, o código escrito após o `yield` é executado:

- `print("Encerrando a API...")`
- fechar conexões com banco;
- encerrar sessões;
- liberar recursos.

## Regra prática

Em FastAPI, a lógica de inicialização da base de dados deve ir antes do `yield`, e a limpeza final deve ir depois dele.

### Ordem correta

1. Preparar aplicação.
2. Criar tabelas / inicializar banco.
3. `yield`.
4. Aplicação em execução.
5. Encerramento da API.
6. Fechar recursos depois do `yield`.

## Exemplo de uso em projeto

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.database import adicionar_livros_default, criar_db_tabelas
from api.routers import livros_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a API...")
    print("Criando tabelas no banco de dados...")
    criar_db_tabelas()
    adicionar_livros_default()
    yield

app = FastAPI(title="API de Livros", lifespan=lifespan)
app.include_router(livros_router.router)
```

Esse padrão é a forma mais comum de garantir que o banco esteja pronto antes que a API comece a atender requisições.
