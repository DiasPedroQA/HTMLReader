"""
Testes para a classe Pasta,
responsável por representar
e manipular diretórios no sistema de arquivos.
"""

from tempfile import TemporaryDirectory
from pathlib import Path
from collections.abc import Generator
from typing import Any
import pytest

from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta


class TestPasta:
    """Testes para os métodos e propriedades da classe Pasta."""

    @pytest.fixture()
    def estrutura_teste(self) -> Generator[Path, Any, None]:
        """
        Cria uma estrutura temporária de pastas e arquivos para testes.

        Returns:
            Path: Caminho da pasta temporária criada.
        """
        with TemporaryDirectory() as tmpdir:
            raiz: Path = Path(tmpdir)
            (raiz / "arquivo1.txt").write_text(data="conteúdo")
            (raiz / ".oculto.txt").write_text(data="oculto")
            sub: Path = raiz / "sub"
            sub.mkdir()
            (sub / "arquivo2.md").write_text(data="conteúdo 2")
            (sub / "outro.log").write_text(data="log")
            yield raiz

    def test_nome_pasta(self, estrutura_teste: Path) -> None:
        """Verifica se o nome da pasta é formatado corretamente."""
        pasta = Pasta(caminho=estrutura_teste)
        assert pasta.nome_pasta == estrutura_teste.stem

    def test_quantidade_arquivos(self, estrutura_teste: Path) -> None:
        """Verifica a contagem correta de arquivos diretos."""
        pasta = Pasta(caminho=estrutura_teste)
        assert pasta.quantidade_arquivos == 2

    def test_quantidade_pastas(self, estrutura_teste: Path) -> None:
        """Verifica a contagem de subdiretórios diretos."""
        pasta = Pasta(caminho=estrutura_teste)
        assert pasta.quantidade_pastas == 1

    def test_existe_arquivo_oculto(self, estrutura_teste: Path) -> None:
        """Verifica se detecta arquivos ocultos corretamente."""
        pasta = Pasta(caminho=estrutura_teste)
        assert pasta.existe_arquivo_oculto is True

    def test_data_modificacao_legivel(self, estrutura_teste: Path) -> None:
        """Verifica se retorna a data de modificação formatada."""
        pasta = Pasta(caminho=estrutura_teste)
        assert isinstance(pasta.data_modificacao_legivel, str)

    def test_coletar_itens_ocultos(self, estrutura_teste: Path) -> None:
        """Verifica se retorna os arquivos ocultos corretamente."""
        pasta = Pasta(caminho=estrutura_teste)
        ocultos: list[Path] = pasta.coletar_itens_ocultos()
        assert any(".oculto" in str(p) for p in ocultos)

    def test_coletar_itens_recursivamente(self, estrutura_teste: Path) -> None:
        """Verifica se retorna corretamente todos os arquivos/pastas de forma recursiva."""
        pasta = Pasta(caminho=estrutura_teste)
        itens: list[CaminhoBase] = pasta.coletar_itens_recursivamente()
        nomes: list[str] = [i.nome_caminho for i in itens]
        assert "arquivo2.md" in nomes
        assert "outro.log" in nomes

    def test_tamanho_total_legivel(self, estrutura_teste: Path) -> None:
        """Verifica se retorna o tamanho total em formato legível."""
        pasta = Pasta(caminho=estrutura_teste)
        assert isinstance(pasta.tamanho_total_legivel, str)

    def test_contar_por_extensao(self, estrutura_teste: Path) -> None:
        """Verifica se conta arquivos por extensão corretamente."""
        pasta = Pasta(caminho=estrutura_teste)
        resultado: dict[str, int] = pasta.contar_por_extensao()
        assert resultado[".log"] == 1
        assert resultado[".txt"] == 2
        # assert resultado[".html"] == 1
