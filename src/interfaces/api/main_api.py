"""
Ponto de entrada da API FastAPI do HTMLReader.

Inclui os roteadores de conversão, pastas, processamento e visualização,
expondo endpoints para manipulação de arquivos e pastas.
"""

from fastapi import FastAPI
from interfaces.api.routes.conversao_router import conversao_router
from interfaces.api.routes.pasta_router import pasta_router
from interfaces.api.routes.processador_routes import processador_router
from interfaces.api.routes.visor_routes import visor_router

app = FastAPI(
    title="HTMLReader API",
    description="API para leitura, análise e processamento de arquivos HTML e texto.",
    version="0.1.0",
)

# Inclusão das rotas específicas de cada domínio
app.include_router(conversao_router, prefix="/conversao", tags=["Conversão"])
app.include_router(pasta_router, prefix="/pasta", tags=["Pastas"])
app.include_router(processador_router, prefix="/processador", tags=["Processamento"])
app.include_router(visor_router, prefix="/visor", tags=["Visualização"])


@app.get("/")
async def root() -> dict[str, str]:
    """
    Rota principal da API para verificação de status.
    """
    return {"message": "Bem-vindo à API do HTMLReader"}
