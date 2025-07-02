"""
Testes unitários para o controlador SistemaController, responsável por obter
informações do sistema operacional atual.

Abrange:
- Teste real com sistema operacional local
- Testes simulados para Linux, Windows e macOS (via mock)
"""

from unittest.mock import patch

import pytest

from core.controllers.sistema_controller import SistemaController
from core.models.sistema_info import SistemaInfo


def test_controller_retorna_modelo_valido() -> None:
    """
    Testa se o SistemaController retorna um objeto SistemaInfo válido
    com informações coerentes no ambiente operacional atual.
    """
    controller = SistemaController(versao_api="1.0.1")
    info: SistemaInfo = controller.obter_info()

    assert info.sistema_operacional in ["Linux", "Windows", "Darwin"]
    assert isinstance(info.diretorio_atual, str)
    assert info.separador_diretorio in ["/", "\\"]
    assert info.versao_api == "1.0.1"
    assert isinstance(info.tempo_desde_boot, str)
    assert isinstance(info.codificacao_padrao, str)


@pytest.mark.parametrize(
    argnames="sistema, versao, arquitetura, nome_maquina, separador",
    argvalues=[
        ("Windows", "10.0.22621", "AMD64", "WIN-PC", "\\"),
        ("Linux", "5.15.0", "x86_64", "linux-machine", "/"),
        ("Darwin", "23.4.0", "arm64", "macbook-pro", "/"),
    ],
)
def test_controller_simulacoes_multiplas(
    sistema: str,
    versao: str,
    arquitetura: str,
    nome_maquina: str,
    separador: str,
) -> None:
    """
    Testa o comportamento do SistemaController simulando diferentes sistemas operacionais
    (Windows, Linux e macOS), usando mocks para simular o ambiente de execução.
    """
    with (
        patch("platform.system", return_value=sistema),
        patch("platform.version", return_value=versao),
        patch("platform.machine", return_value=arquitetura),
        patch("platform.node", return_value=nome_maquina),
        patch("os.sep", separador),
    ):
        controller = SistemaController(versao_api="1.0.1")
        info: SistemaInfo = controller.obter_info()

        assert info.sistema_operacional == sistema
        assert info.arquitetura == arquitetura
        assert info.nome_maquina == nome_maquina
        assert info.separador_diretorio == separador
        assert info.versao_api == "1.0.1"
