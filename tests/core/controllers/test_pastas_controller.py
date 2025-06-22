# pylint: disable=W0621

"""
Testes automatizados para o controlador PastasController
responsável por operações com diretórios.
"""

from pathlib import Path
import pytest

from core.controllers.pastas_controller import PastasController
from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta


@pytest.fixture
def controlador() -> PastasController:
    """Instancia o controlador a ser usado nos testes."""
    return PastasController()


class TestPastasController:
    """
    Classe de testes para a `PastasController`,
    que gerencia diretórios do sistema de arquivos.
    """

    def test_criar_pasta_se_nao_existir(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve criar uma nova pasta se ela não existir e retornar False se já existir."""
        caminho: Path = tmp_path / "nova"
        assert not caminho.exists()
        assert controlador.criar_pasta_se_nao_existir(caminho_novo=caminho) is True
        assert caminho.exists()
        assert controlador.criar_pasta_se_nao_existir(caminho_novo=caminho) is False

    def test_ler_nomes_dos_itens_da_pasta(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve retornar os nomes de arquivos e subpastas imediatos na pasta fornecida."""
        (tmp_path / "arquivo.txt").touch()
        (tmp_path / "subpasta").mkdir()
        nomes: list[str] = controlador.ler_nomes_dos_itens_da_pasta(caminho=tmp_path)
        assert set(nomes) == {"arquivo.txt", "subpasta"}

    def test_coletar_itens_ocultos(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve retornar apenas os arquivos e pastas ocultos (prefixados com ponto)."""
        (tmp_path / ".oculto.txt").touch()
        (tmp_path / ".ocultapasta").mkdir()
        (tmp_path / "visivel.txt").touch()
        nomes_ocultos: set[str] = {
            p.name for p in controlador.coletar_itens_ocultos(caminho=tmp_path)
        }
        assert ".oculto.txt" in nomes_ocultos
        assert ".ocultapasta" in nomes_ocultos
        assert "visivel.txt" not in nomes_ocultos

    def test_ler_sub_pastas_de_uma_pasta(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve retornar todas as subpastas imediatas da pasta informada."""
        (tmp_path / "sub1").mkdir()
        (tmp_path / "sub2").mkdir()
        (tmp_path / "arquivo.txt").touch()
        subpastas: list[Pasta] = controlador.ler_sub_pastas_de_uma_pasta(
            caminho_da_pasta=tmp_path
        )
        nomes: list[str] = [p.nome_caminho for p in subpastas]
        assert set(nomes) == {"sub1", "sub2"}

    def test_ler_sub_arquivos_de_uma_pasta(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve retornar apenas arquivos (com ou sem filtro de extensão)."""
        (tmp_path / "pasta").mkdir()
        (tmp_path / "pasta/a.txt").touch()
        (tmp_path / "pasta/b.py").touch()

        arquivos_txt: list[Arquivo] = controlador.ler_sub_arquivos_de_uma_pasta(
            caminho_da_pasta=tmp_path, extensao_buscada=".txt"
        )
        assert [a.nome_caminho for a in arquivos_txt] == []

        todos: list[Arquivo] = controlador.ler_sub_arquivos_de_uma_pasta(
            caminho_da_pasta=tmp_path
        )
        nomes: list[str] = [a.nome_caminho for a in todos]
        assert "a.txt" not in nomes
        assert "b.py" not in nomes
        assert "pasta" not in nomes

    def test_ler_recursivamente_caminhos_da_pasta(
        self, tmp_path: Path, controlador: PastasController
    ) -> None:
        """Deve retornar todos os caminhos internos (arquivos e pastas), de forma recursiva."""
        (tmp_path / "sub1").mkdir()
        (tmp_path / "sub1" / "a.txt").touch()
        (tmp_path / "arquivo.txt").touch()
        caminhos: list[CaminhoBase] = controlador.ler_recursivamente_caminhos_da_pasta(
            caminho=tmp_path
        )
        nomes: list[str] = [caminho.nome_caminho for caminho in caminhos]
        assert "a.txt" in nomes
        assert "arquivo.txt" in nomes
