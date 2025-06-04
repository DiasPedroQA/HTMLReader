"""
Rotas da API para o visor de arquivos e pastas do HTMLReader.

Inclui endpoints para listar o conteúdo de diretórios e obter prévias de arquivos.
"""

from fastapi import APIRouter
from htmlreader.core.models.visor_models import (
    CaminhoEntrada,
    FiltroVisor,
    ListaDeItens,
    PreviaArquivo,
)
from htmlreader.core.services import visor_service

router = APIRouter()


@router.post("/listar", response_model=ListaDeItens)
def listar(body: dict):
    """
    Endpoint para listar o conteúdo de um diretório.

    Args:
        body (dict): Deve conter as chaves 'caminho' (dict) e 'filtros' (dict, opcional).

    Returns:
        ListaDeItens: Lista dos itens encontrados no diretório.
    """
    caminho = (
        CaminhoEntrada(**body["caminho"])
        if isinstance(body["caminho"], dict)
        else CaminhoEntrada(path=body["caminho"])
    )
    filtros = (
        FiltroVisor(**body["filtros"])
        if "filtros" in body and body["filtros"] is not None
        else FiltroVisor()
    )
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
