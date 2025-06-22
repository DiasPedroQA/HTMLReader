"""
Testes unitários para a enumeração e métodos utilitários de `SistemaOperacional`.

Este conjunto de testes cobre:
- Detecção do sistema operacional com e sem simulação
- Obtenção de caminho raiz do usuário conforme o sistema
- Tratamento de sistemas não suportados

Os testes são parametrizados com exemplos comuns de sistemas operacionais conhecidos.
"""

import re
from pathlib import Path

import pytest

from core.utils.sistema_operacional import SistemaOperacional


class TestSistemaOperacional:
    """Classe de testes para os métodos da enumeração `SistemaOperacional`."""

    @pytest.mark.parametrize(
        "entrada, esperado",
        [
            ("windows", SistemaOperacional.WINDOWS),
            ("Windows 11", SistemaOperacional.WINDOWS),
            ("linux", SistemaOperacional.LINUX),
            ("LINUX Mint", SistemaOperacional.LINUX),
            ("mac", SistemaOperacional.MACOS),
            ("macos", SistemaOperacional.MACOS),
            ("Darwin", SistemaOperacional.MACOS),
        ],
    )
    def test_detectar_sistema_operacional_valido(self, entrada: str, esperado: SistemaOperacional) -> None:
        """Verifica se a detecção do sistema retorna a enumeração esperada."""
        resultado: SistemaOperacional = SistemaOperacional.detectar(sistema_simulado=entrada)
        assert resultado == esperado

    @pytest.mark.parametrize("sistema_invalido", ["beos", "atari", "plan9"])
    def test_detectar_sistema_operacional_invalido(self, sistema_invalido: str) -> None:
        """Verifica se uma exceção é lançada para sistemas não suportados."""
        with pytest.raises(expected_exception=ValueError, match="Sistema não suportado"):
            SistemaOperacional.detectar(sistema_simulado=sistema_invalido)

    @pytest.mark.parametrize(
        "sistema, esperado_prefixo",
        [
            ("windows", Path("C:/Users/")),
            ("linux", Path("/home/")),
            ("macos", Path("/Users/")),
        ],
    )
    def test_obter_raiz_usuario_com_sistema_simulado(self, sistema: str, esperado_prefixo: Path) -> None:
        """Verifica se o caminho raiz do usuário simulado começa com o prefixo esperado."""
        caminho: Path = SistemaOperacional.obter_raiz_usuario(sistema_desejado=sistema)
        assert isinstance(caminho, Path)
        assert str(caminho).startswith(str(esperado_prefixo))

    def test_obter_raiz_usuario_com_sistema_invalido(self) -> None:
        """Garante que sistemas inválidos geram exceção ao obter raiz do usuário."""
        sistema_invalido: str = "android"

        with pytest.raises(
            expected_exception=ValueError,
            match=re.escape(f"Sistema não suportado: {sistema_invalido} (processado: {sistema_invalido})"),
        ):
            SistemaOperacional.obter_raiz_usuario(sistema_desejado=sistema_invalido)
