"""
Testes unitários para a classe Pasta,
responsável pela manipulação de diretórios no sistema de arquivos.
"""

from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta


class TestPasta:
    """Testa os métodos e propriedades públicas da classe Pasta."""

    @pytest.fixture()
    def estrutura_temporaria(self) -> Generator[Path, Any, None]:
        """
        Cria uma estrutura de diretórios e arquivos para os testes.

        Retorna:
            Generator[Path, Any, None]: Caminho da pasta raiz temporária.
        """
        with TemporaryDirectory() as tmpdir:
            raiz = Path(tmpdir)
            (raiz / "arquivo1.txt").write_text(data="conteúdo")
            (raiz / ".oculto.txt").write_text(data="oculto")
            subpasta: Path = raiz / "sub"
            subpasta.mkdir()
            (subpasta / "arquivo2.md").write_text(data="conteúdo 2")
            (subpasta / "outro.log").write_text(data="log")
            yield raiz

    def test_nome_formatado_da_pasta(self, estrutura_temporaria: Path) -> None:
        """Deve retornar o nome formatado da pasta raiz."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert pasta.nome == estrutura_temporaria.stem

    def test_conta_arquivos_diretos(self, estrutura_temporaria: Path) -> None:
        """Deve contar corretamente os arquivos diretamente contidos."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert pasta.total_arquivos == 2

    def test_conta_subpastas_diretas(self, estrutura_temporaria: Path) -> None:
        """Deve contar corretamente as subpastas diretamente contidas."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert pasta.total_subpastas == 1

    def test_detecta_arquivos_ocultos(self, estrutura_temporaria: Path) -> None:
        """Deve detectar arquivos ocultos diretamente contidos."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert pasta.possui_ocultos is True

    def test_retorna_data_modificacao_formatada(self, estrutura_temporaria: Path) -> None:
        """Deve retornar a data de modificação da pasta em formato string."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert isinstance(pasta.data_modificacao_formatada, str)

    def test_lista_arquivos_ocultos(self, estrutura_temporaria: Path) -> None:
        """Deve retornar os caminhos dos arquivos ocultos diretamente contidos."""
        pasta = Pasta(caminho=estrutura_temporaria)
        ocultos: list[Path] = pasta.listar_ocultos()
        assert any(".oculto" in p.name for p in ocultos)

    def test_lista_conteudo_recursivamente(self, estrutura_temporaria: Path) -> None:
        """Deve retornar todos os arquivos e pastas contidos, de forma recursiva."""
        pasta = Pasta(caminho=estrutura_temporaria)
        itens: list[CaminhoBase] = pasta.listar_conteudo_recursivo()
        nomes: list[str] = [item.nome_caminho for item in itens]
        assert "arquivo2.md" in nomes
        assert "outro.log" in nomes

    def test_tamanho_total_em_formato_legivel(self, estrutura_temporaria: Path) -> None:
        """Deve retornar o tamanho da pasta em formato de leitura humana (ex: MB)."""
        pasta = Pasta(caminho=estrutura_temporaria)
        assert isinstance(pasta.tamanho_formatado, str)

    def test_conta_arquivos_por_extensao(self, estrutura_temporaria: Path) -> None:
        """Deve contar corretamente os arquivos por extensão."""
        pasta = Pasta(caminho=estrutura_temporaria)
        resultado: dict[str, int] = pasta.contar_extensoes()
        assert resultado[".log"] == 1
        assert resultado[".txt"] == 2
