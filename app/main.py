from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base

from app.models.aluno_model import Aluno
from app.models.pagamento_model import Pagamento
from app.models.produto_model import Produto

from app.routes.aluno_routes import router as aluno_router
from app.routes.pagamento_routes import router as pagamento_router
from app.routes.relatorio_routes import router as relatorio_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.produto_routes import router as produto_router

from contextlib import asynccontextmanager

from app.scheduler.scheduler import (
    iniciar_scheduler,
    scheduler
)

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    #iniciar_scheduler()

    yield

    scheduler.shutdown()

app = FastAPI(
    title="Academy System API",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aluno_router)
app.include_router(pagamento_router)
app.include_router(dashboard_router)
app.include_router(relatorio_router)
app.include_router(produto_router)


@app.get("/")
def home():
    return {
        "message": "Sistema Academia API"
    }