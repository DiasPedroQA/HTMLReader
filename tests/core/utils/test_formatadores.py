"""
Testes unitários para o módulo de formatação de dados de arquivos.
"""

import time
from datetime import datetime

import pytest

from core.utils.formatadores import (
    formatar_arquivo_data_para_string,
    formatar_arquivo_obter_extensao_legivel,
    formatar_arquivo_tamanho_legivel,
    formatar_arquivo_valor_booleano,
)


class TestFormatadores:
    """Classe de testes para funções de formatação de arquivos."""

    @pytest.mark.parametrize(
        argnames="tamanho_bytes, esperado",
        argvalues=[
            (0, "0.00 B"),
            (1, "1.00 B"),
            (1023, "1023.00 B"),
            (1024, "1.00 KB"),
            (1536, "1.50 KB"),
            (1024 * 1024, "1.00 MB"),
            (2.5 * 1024 * 1024, "2.50 MB"),
            (1024 * 1024 * 1024, "1.00 GB"),
            (1024 * 1024 * 1024 * 1024, "1.00 TB"),
            (-1, "0.00 B"),
        ],
    )
    def test_formatar_arquivo_tamanho_legivel(
        self, tamanho_bytes: int | float, esperado: str
    ) -> None:
        """Testa a formatação de tamanhos de arquivo em bytes para uma string legível."""
        assert formatar_arquivo_tamanho_legivel(tamanho_bytes=tamanho_bytes) == esperado

    def test_formatar_arquivo_data_para_string(self) -> None:
        """Testa a formatação de timestamps para strings de data legíveis."""
        # Timestamp conhecido (01/01/2020 00:00:00 UTC)
        timestamp = 5577836800
        assert (
            formatar_arquivo_data_para_string(float_data_e_hora=timestamp)
            == "03/10/2146 04:06:40"
        )

        # Data atual
        now: float = time.time()
        formatted: str = formatar_arquivo_data_para_string(float_data_e_hora=now)
        assert datetime.strptime(formatted, "%d/%m/%Y %H:%M:%S")  # Verifica se é válido

        # Timestamp zero (01/01/1970)
        assert "1969" in formatar_arquivo_data_para_string(float_data_e_hora=0)

    @pytest.mark.parametrize(
        argnames="extensao, esperado",
        argvalues=[
            (".txt", "Texto"),
            (".md", "Markdown"),
            ("json", "JSON"),
            (".PY", "Script Python"),
            (".xyz", "XYZ"),
            ("", ""),
        ],
    )
    def test_formatar_arquivo_obter_extensao_legivel(
        self, extensao: str, esperado: str
    ) -> None:
        """Teste parametrizado para formatação de extensões."""
        assert (
            formatar_arquivo_obter_extensao_legivel(extensao_arquivo=extensao)
            == esperado
        )

    @pytest.mark.parametrize(
        argnames="valor, esperado",
        argvalues=[
            (True, "Sim"),
            (False, "Não"),
            (1, "Sim"),
            (0, "Não"),
            ([], "Não"),
            ([1], "Sim"),
            (None, "Não"),
        ],
    )
    def test_formatar_arquivo_valor_booleano(
        self, valor: list[int] | None | bool | str, esperado: str
    ) -> None:
        """Testa a conversão de valores booleanos para 'Sim'/'Não'."""
        assert formatar_arquivo_valor_booleano(valor=valor) == esperado
        assert formatar_arquivo_valor_booleano(valor=True) == "Sim"
        assert formatar_arquivo_valor_booleano(valor=False) == "Não"

        # Truthy/falsy values
        # assert formatar_arquivo_valor_booleano(valor=bool(1)) == "Sim"
        # assert formatar_arquivo_valor_booleano(valor=bool(0)) == "Não"
        # assert formatar_arquivo_valor_booleano(valor=bool([])) == "Não"
        # assert formatar_arquivo_valor_booleano(valor=bool([1])) == "Sim"

    @pytest.mark.parametrize(
        argnames="tamanho_arquivo, esperado",
        argvalues=[
            (0, "0.00 B"),
            (1023, "1023.00 B"),
            (1024, "1.00 KB"),
            (1024 * 1024, "1.00 MB"),
            (1024 * 1024 * 1024, "1.00 GB"),
            (1024 * 1024 * 1024 * 1024, "1.00 TB"),
            (1536, "1.50 KB"),
            (1.5 * 1024 * 1024, "1.50 MB"),
        ],
    )
    def test_formatar_arquivo_tamanho_legivel_parametrizado(
        self, tamanho_arquivo: int | float, esperado: str
    ) -> None:
        """Teste parametrizado para formatação de tamanhos."""
        assert (
            formatar_arquivo_tamanho_legivel(tamanho_bytes=tamanho_arquivo) == esperado
        )

    @pytest.mark.parametrize(
        argnames="extensao, esperado",
        argvalues=[
            (".txt", "Texto"),
            (".md", "Markdown"),
            ("json", "JSON"),
            (".PY", "Script Python"),
            (".xyz", "XYZ"),
            ("", ""),
        ],
    )
    def test_formatar_arquivo_obter_extensao_legivel_parametrizado(
        self, extensao: str, esperado: str
    ) -> None:
        """Teste parametrizado para formatação de extensões."""
        assert (
            formatar_arquivo_obter_extensao_legivel(extensao_arquivo=extensao)
            == esperado
        )
