"""
Testes unitários para o módulo de representação e manipulação de arquivos no sistema de arquivos.

Este conjunto de testes valida o comportamento da classe `Arquivo`, garantindo que
suas propriedades e métodos funcionem corretamente. Os testes cobrem:

- Manipulação de extensão e nomes de arquivos
- Detecção de arquivos ocultos
- Leitura e escrita de conteúdo
- Criação condicional de arquivos
- Acesso a metadados como tamanho, data de criação e modificação

Requer que a classe `Arquivo` esteja implementada corretamente e que o módulo
`core.models.model_arquivo` esteja acessível.
"""

from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from core.models.model_arquivo import Arquivo


class TestArquivo:
    """
    Testes unitários para a classe Arquivo, responsável por representar arquivos
    no sistema de arquivos com métodos de leitura, escrita, verificação de metadados
    e análise de propriedades como nome, extensão e visibilidade.
    """

    @pytest.fixture()
    def arquivo_teste(self) -> Generator[Path, Any, None]:
        """
        Fixture que cria um arquivo temporário com conteúdo de teste.

        Returns:
            Path: Caminho do arquivo temporário criado.
        """
        with TemporaryDirectory() as tmpdir:
            caminho: Path = Path(tmpdir) / "teste.txt"
            caminho.write_text(data="conteúdo de teste", encoding="utf-8")
            yield caminho

    def test_nome_sem_extensao(self, arquivo_teste: Path) -> None:
        """Deve retornar corretamente o nome do arquivo sem a extensão."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert arquivo.nome_sem_extensao == "teste"

    def test_extensao(self, arquivo_teste: Path) -> None:
        """Deve retornar a extensão correta do arquivo."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert arquivo.extensao == ".txt"

    def test_extensao_legivel(self, arquivo_teste: Path) -> None:
        """Deve retornar uma descrição legível da extensão do arquivo."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert arquivo.extensao_legivel == "Texto"

    def test_tamanho_legivel(self, arquivo_teste: Path) -> None:
        """Deve retornar o tamanho do arquivo em formato legível."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert isinstance(arquivo.tamanho_legivel, str)

    def test_data_modificacao_legivel(self, arquivo_teste: Path) -> None:
        """Deve retornar a data de modificação do arquivo em formato legível."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert isinstance(arquivo.data_modificacao_legivel, str)

    def test_data_criacao_legivel(self, arquivo_teste: Path) -> None:
        """Deve retornar a data de criação do arquivo em formato legível."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert isinstance(arquivo.data_criacao_legivel, str)

    def test_eh_arquivo_oculto(self, arquivo_teste: Path) -> None:
        """Deve identificar corretamente arquivos ocultos."""
        oculto: Path = arquivo_teste.parent / ".oculto.txt"
        oculto.write_text(data="arquivo oculto", encoding="utf-8")
        arquivo = Arquivo(caminho=oculto)
        assert arquivo.eh_arquivo_oculto is True

    def test_diretorio_pai(self, arquivo_teste: Path) -> None:
        """Deve retornar corretamente o diretório pai do arquivo."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert arquivo.diretorio_pai == arquivo_teste.parent

    def test_criar_arquivo_se_nao_existir(self) -> None:
        """Deve criar um novo arquivo quando ele não existir."""
        with TemporaryDirectory() as tmpdir:
            caminho: Path = Path(tmpdir) / "novo.txt"
            arquivo = Arquivo(caminho=caminho)
            resultado: bool = arquivo.criar_arquivo_se_nao_existir()
            assert resultado is True
            assert caminho.exists()

    def test_escrever_conteudo(self, arquivo_teste: Path) -> None:
        """Deve sobrescrever o conteúdo do arquivo quando permitido."""
        arquivo = Arquivo(caminho=arquivo_teste)
        resultado: bool = arquivo.escrever_conteudo(conteudo_arquivo="novo conteudo", sobrescrever=True)
        assert resultado is True
        assert arquivo.ler_conteudo() == "novo conteudo"

    def test_nao_sobrescrever_arquivo_existente(self, arquivo_teste: Path) -> None:
        """Não deve sobrescrever o arquivo quando a sobrescrição não é permitida."""
        arquivo = Arquivo(caminho=arquivo_teste)
        resultado: bool = arquivo.escrever_conteudo(conteudo_arquivo="ignorado", sobrescrever=False)
        assert resultado is False

    def test_ler_conteudo(self, arquivo_teste: Path) -> None:
        """Deve ler corretamente o conteúdo existente no arquivo."""
        arquivo = Arquivo(caminho=arquivo_teste)
        assert arquivo.ler_conteudo() == "conteúdo de teste"

    def test_ler_conteudo_inexistente(self) -> None:
        """Deve retornar None ao tentar ler conteúdo de arquivo inexistente."""
        arquivo = Arquivo(caminho=Path("/caminho/inexistente.txt"))
        assert arquivo.ler_conteudo() is None
