"""
Módulo de rotas para a API REST relacionadas às informações do sistema operacional.

Define endpoints que expõem dados coletados pelo SistemaController, incluindo
detalhes como versão, arquitetura, diretórios e tempo desde o último boot.

Esta API é consumida por clientes que precisam de diagnóstico ou configuração
dinâmica baseada no ambiente da máquina.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.controllers.sistema_controller import SistemaController
from app.core.models.sistema_info import SistemaInfo

router = APIRouter(prefix="/sistema", tags=["Sistema"])


def get_sistema_controller() -> SistemaController:
    """
    Cria e retorna uma instância do SistemaController.

    Pode ser facilmente substituído em testes para mocks ou variações.
    """
    return SistemaController(versao_api="1.0.1")


@router.get(
    path="/info",
    name="obter_informacoes_sistema",
    response_model=SistemaInfo,
    summary="Obter informações do sistema operacional",
    description=(
        "Retorna dados detalhados do sistema operacional atual, "
        "como versão, arquitetura, diretórios e tempo desde o último boot."
    ),
)
def obter_informacoes_sistema(
    controller: SistemaController = Depends(dependency=get_sistema_controller),
) -> SistemaInfo:
    """
    Endpoint para obter as informações do sistema operacional.

    Args:
        controller (SistemaController): Instância injetada do controlador.

    Returns:
        SistemaInfo: Modelo com dados do sistema.

    Raises:
        HTTPException: Se ocorrer erro inesperado ao obter informações do sistema.
    """
    try:
        info: SistemaInfo = controller.obter_info()
    except Exception as e:
        # Em caso de erro inesperado, retorna 500 Internal Server Error, preservando stack trace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do sistema: {str(e)}",
        ) from e
    return info
