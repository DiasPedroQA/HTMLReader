"""
Ponto de entrada da API FastAPI do HTMLReader.

Inclui os roteadores de visor e processador,
expondo endpoints para manipulação de arquivos e pastas.
"""

from fastapi import FastAPI
from .routes import visor_routes, processador_routes

app = FastAPI(title="HTMLReader API")

app.include_router(visor_routes.router, prefix="/visor", tags=["Visor"])
app.include_router(
    processador_routes.router, prefix="/processador", tags=["Processador"]
)
