from fastapi import FastAPI
import uvicorn as uv
from api.handlers.auth_handlers import register_auth_handlers
from api.routes.router import router as diagnose_router

app = FastAPI(
    title="SolveDesk Agent API",
    description="API do inteligentnego wyszukiwania i analizy podobnych zgłoszeń przy użyciu modeli BERT",
    version="1.01.001"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#register_auth_handlers(app)

app.include_router(diagnose_router, prefix="/api", tags=["Diagnose"])

if __name__ == "__main__":
    uv.run("main:app", host="127.0.0.1", port=8080, reload=True)