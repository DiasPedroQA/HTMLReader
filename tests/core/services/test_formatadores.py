"""
Testes unitários para o módulo `formatadores`.

Este módulo contém testes para funções auxiliares de formatação de:
- tamanhos em bytes para representação legível
- datas para string
- extensões de arquivos para nomes amigáveis
- valores booleanos para texto ("Sim"/"Não")
- nomes de arquivos truncados

Utiliza `pytest` e `pytest.mark.parametrize` para testes parametrizados.
"""

from datetime import datetime
from typing import LiteralString
import pytest

from core.services.formatadores import (
    converter_bytes_em_tamanho_legivel,
    formatar_data_para_string,
    obter_extensao_legivel,
    formatar_booleano,
    formatar_nome_arquivo,
)


class TestFormatadores:
    """Classe de testes para as funções do módulo `formatadores`."""

    def test_converter_bytes_em_tamanho_legivel(self) -> None:
        """Verifica a conversão correta de valores em bytes para string legível."""
        assert converter_bytes_em_tamanho_legivel(tamanho_bytes=1023) == "1023.00 B"
        assert converter_bytes_em_tamanho_legivel(tamanho_bytes=1024) == "1.00 KB"
        assert converter_bytes_em_tamanho_legivel(tamanho_bytes=1048576) == "1.00 MB"
        assert converter_bytes_em_tamanho_legivel(tamanho_bytes=0) == "0.00 B"

    def test_formatar_data_para_string(self) -> None:
        """Verifica se uma data é formatada corretamente no padrão 'dd/mm/aaaa HH:MM:SS'."""
        data = datetime(year=2024, month=6, day=1, hour=15, minute=30, second=45)
        assert formatar_data_para_string(data_e_hora=data) == "01/06/2024 15:30:45"

    @pytest.mark.parametrize(
        argnames="entrada, esperado",
        argvalues=[
            (".txt", "Texto"),
            (".md", "Markdown"),
            (".json", "JSON"),
            (".csv", "Planilha CSV"),
            (".py", "Script Python"),
            (".xml", "XML"),
            (".html", "HTML"),
            (".log", "Log"),
            (".xyz", "XYZ"),
            ("sem_ponto", "SEM_PONTO"),
        ],
    )
    def test_obter_extensao_legivel(self, entrada: str, esperado: str) -> None:
        """Verifica se extensões são convertidas para nomes amigáveis corretamente."""
        assert obter_extensao_legivel(formato_padrao_extensao=entrada) == esperado

    @pytest.mark.parametrize(
        argnames="entrada, esperado",
        argvalues=[
            (True, "Sim"),
            (False, "Não"),
        ],
    )
    def test_formatar_booleano(self, entrada: bool, esperado: str) -> None:
        """Testa a conversão de valores booleanos para 'Sim' ou 'Não'."""
        assert formatar_booleano(valor=entrada) == esperado

    def test_formatar_nome_arquivo(self) -> None:
        """Verifica truncamento de nomes longos e preservação de nomes curtos."""
        nome_curto = "arquivo.txt"
        assert formatar_nome_arquivo(nome=nome_curto) == nome_curto

        nome_longo: LiteralString = "a" * 60
        assert formatar_nome_arquivo(nome=nome_longo, limite=50) == ("a" * 47 + "...")
