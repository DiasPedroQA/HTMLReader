"""
Rotas da API para processamento de arquivos no HTMLReader.

Inclui endpoints para processar um único arquivo ou um lote de arquivos,
retornando os resultados do processamento.
"""

from fastapi import APIRouter

from htmlreader.core.models.processador_models import (
    CaminhoArquivo,
    LoteDeArquivos,
    ResultadoProcessamento,
)
from htmlreader.core.services import processador_service

router = APIRouter()


@router.post("/unique", response_model=ResultadoProcessamento)
def processar_arquivo(entrada: CaminhoArquivo):
    """
    Endpoint para processar um único arquivo.

    Args:
        entrada (CaminhoArquivo): Modelo contendo o caminho do arquivo a ser processado.

    Returns:
        ResultadoProcessamento: Resultado do processamento do arquivo.
    """
    return processador_service.processar_arquivo(entrada.path)


@router.post("/lote", response_model=list[ResultadoProcessamento])
def processar_lote(lote: LoteDeArquivos):
    """
    Endpoint para processar um lote de arquivos.

    Args:
        lote (LoteDeArquivos): Modelo contendo a lista de arquivos a serem processados.

    Returns:
        list[ResultadoProcessamento]: Lista de resultados do
        processamento de cada arquivo.
    """
    return processador_service.processar_em_lote(lote)
