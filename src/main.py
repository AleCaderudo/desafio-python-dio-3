from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.tables import metadata

    # 👉 ENGINE 100% SÍNCRONO PARA CRIAR AS TABELAS
    sync_engine = create_engine("sqlite:///db.sqlite3", connect_args={"check_same_thread": False})
    metadata.create_all(sync_engine)

    # 👉 conecta no banco async depois
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

#acesso na raiz do app
@app.get("/")
def root(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "message": "API Desafio Bank está no ar!",
        "docs": f"{base_url}/docs",
        "redoc": f"{base_url}/redoc"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)
