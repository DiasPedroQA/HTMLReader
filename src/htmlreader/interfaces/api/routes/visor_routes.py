"""
Rotas da API para o visor de arquivos e pastas do HTMLReader.

Inclui endpoints para listar o conteúdo de diretórios e obter prévias de arquivos.
"""

from fastapi import APIRouter
from src.htmlreader.core.models.visor_models import (
    CaminhoEntrada,
    FiltroVisor,
    ListaDeItens,
    PreviaArquivo,
)
from src.htmlreader.core.services import visor_service

router = APIRouter()


@router.post("/listar", response_model=ListaDeItens)
def listar(caminho: CaminhoEntrada, filtros: FiltroVisor = FiltroVisor()):
    """
    Endpoint para listar o conteúdo de um diretório.

    Args:
        caminho (CaminhoEntrada): Modelo contendo o caminho do diretório.
        filtros (FiltroVisor, opcional): Filtros para a listagem dos itens.

    Returns:
        ListaDeItens: Lista dos itens encontrados no diretório.
    """
    return visor_service.listar_conteudo(caminho.path, filtros)


@router.post("/previa", response_model=PreviaArquivo)
def previa(caminho: CaminhoEntrada):
    """
    Endpoint para obter uma prévia de um arquivo.

    Args:
        caminho (CaminhoEntrada): Modelo contendo o caminho do arquivo.

    Returns:
        PreviaArquivo: Dados resumidos e linhas iniciais do arquivo.
    """
    return visor_service.obter_previa(caminho.path)
