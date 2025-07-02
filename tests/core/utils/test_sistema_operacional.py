"""
Testes unitários para o módulo 'sistema_operacional'.

Verifica:
- Retorno correto da estrutura `DadosSistemaOperacional`
- Compatibilidade entre diferentes sistemas operacionais
- Robustez do método `obter_dados_usuario`
- Simulações de múltiplos ambientes com uso de `unittest.mock`
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from core.utils.sistema_operacional import (
    DadosSistemaOperacional,
    SistemaOperacional,
)


class TestSistemaOperacional:
    """
    Conjunto de testes para a classe utilitária 'SistemaOperacional'.
    """

    def test_retorno_estrutura_valida(self) -> None:
        """
        Verifica se o método retorna um objeto válido de DadosSistemaOperacional.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert isinstance(dados, DadosSistemaOperacional)
        assert isinstance(dados.nome, str)
        assert isinstance(dados.caminho_usuario, Path)
        assert isinstance(dados.usuario_root, bool)
        assert isinstance(dados.encontrado, bool)

    def test_nome_do_sistema_valido(self) -> None:
        """
        Garante que o nome do sistema detectado esteja entre os suportados.
        """
        nome: str = SistemaOperacional.detectar_nome()
        assert nome in {"linux", "windows", "darwin"}

    def test_caminho_esperado_por_sistema(self) -> None:
        """
        Valida que o caminho do usuário segue o padrão esperado para o SO.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        caminho_str = str(dados.caminho_usuario)

        if dados.nome == "linux":
            assert caminho_str.startswith("/home") or dados.usuario_root
        elif dados.nome == "darwin":
            assert caminho_str.startswith("/Users") or dados.usuario_root
        elif dados.nome == "windows":
            assert ":" in caminho_str
        else:
            assert caminho_str in {"/desconhecido", "/erro"}

    def test_caminho_usuario_existe_ou_tratado(self) -> None:
        """
        Garante que o campo `encontrado` seja coerente com a existência real do caminho.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert dados.encontrado == dados.caminho_usuario.exists()

    def test_nunca_lanca_excecao(self) -> None:
        """
        Confirma que o método nunca lança exceções não tratadas.
        """
        try:
            _: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        except OSError as e:
            pytest.fail(reason=f"Exceção inesperada ao obter dados do sistema: {e}")

    @patch("platform.system", return_value="Windows")
    @patch("os.environ.get", return_value="C:\\Users\\MockedUser")
    def test_simulacao_windows(self, *_) -> None:
        """
        Simula execução em Windows e verifica o caminho do usuário.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert dados.nome == "windows"
        assert "C:\\" in str(dados.caminho_usuario)

    @patch("platform.system", return_value="Darwin")
    def test_simulacao_darwin(self, *_) -> None:
        """
        Simula execução em macOS (Darwin) e verifica o caminho do usuário.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert dados.nome == "darwin"
        assert dados.caminho_usuario == Path.home()

    @patch("platform.system", return_value="FreeBSD")
    def test_simulacao_sistema_desconhecido(self, *_) -> None:
        """
        Simula um sistema operacional não reconhecido e verifica o caminho padrão.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert dados.nome == "freebsd"
        assert dados.caminho_usuario == Path("/desconhecido")
        assert not dados.encontrado

    @patch("platform.system", return_value="Linux")
    @patch("pathlib.Path.home", side_effect=OSError("Erro simulado"))
    def test_simulacao_erro_home(self, *_) -> None:
        """
        Simula falha ao obter o diretório home do usuário.
        """
        dados: DadosSistemaOperacional = SistemaOperacional.obter_dados_usuario()
        assert dados.caminho_usuario == Path("/erro")
        assert not dados.encontrado
