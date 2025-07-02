"""
Ponto de entrada principal da API FastAPI para o projeto HTMLReader.

Inclui as rotas disponíveis e configurações básicas da aplicação.
"""

import uvicorn
from fastapi import FastAPI

# from interfaces.api.routes import infosistema_routes

app = FastAPI(
    title="HTMLReader API",
    version="1.0.0",
    description="API para leitura e análise de arquivos e diretórios HTML no sistema local.",
)

# Inclusão das rotas
# src.include_router(router=infosistema_routes.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="interfaces.api.main_api:app", host="127.0.0.1", port=8000, reload=True)

# caminhos = [
#     "~/Downloads/Firefox",
#     "../../Downloads/Firefox",
#     "~/Downloads/Firefox/bookmarks.html",
#     "../../Downloads/Firefox/bookmarks.html",
#     "/home/pedro-pm-dias/Downloads/Firefox",
#     "/home/pedro-pm-dias/Downloads/Firefox",
#     "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
#     "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
# ]
