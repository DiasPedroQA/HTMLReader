"""
Testes automatizados para o módulo de utilitários de formatação de arquivos e diretórios.

Este conjunto de testes cobre:
- Extração de metadados com `gerar_dados_item`
- Conversão legível de tamanhos com `converter_tamanho`
- Verificação de permissões e tipos de caminho
- Tratamento de erros com `ErroAcessoArquivo`

Testes unitários para o módulo 'sistema_operacional'.

Verifica:
- Retorno correto da estrutura `DadosSistemaOperacional`
- Compatibilidade entre diferentes sistemas operacionais
- Robustez do método `obter_dados_usuario`
- Simulações de múltiplos ambientes com uso de `unittest.mock`
"""

from __future__ import annotations
from pathlib import Path
from os import stat_result
from unittest.mock import patch, MagicMock
import pytest


from src.core.utils.sistema_operacional import (
    DadosSistemaOperacional,
    SistemaOperacional,
)

from src.core.utils.extratores import (
    ErroAcessoArquivo,
    MetadadosArquivo,
    PermissoesDetalhadas,
    Tempos,
    coletar_info_basica,
    coletar_permissoes,
    coletar_tempos,
    converter_tamanho,
    gerar_dados_item,
    validar_caminho,
)


class TestFormatadoresUtilitarios:
    """Testes para funções do módulo extratores."""

    def test_validar_caminho_valido(self, tmp_path: Path) -> None:
        """Testa a validação de caminho válido."""
        file: Path = tmp_path / "arquivo.txt"
        file.write_text(data="conteudo")
        resultado: Path = validar_caminho(caminho=str(file))
        assert isinstance(resultado, Path)
        assert resultado == file

    def test_validar_caminho_invalido(self) -> None:
        """Testa validação com caminho inválido, espera exceção."""
        with pytest.raises(expected_exception=ErroAcessoArquivo):
            validar_caminho(caminho="/caminho/nao/existe")

    def test_validar_caminho_tipo_invalido(self) -> None:
        """Testa validação com tipo inválido, espera TypeError."""
        with pytest.raises(expected_exception=TypeError):
            validar_caminho(caminho="12345")

    @pytest.mark.parametrize(
        argnames="bytes_entrada, resultado_esperado",
        argvalues=[
            (0, "0.00 B"),
            (1023, "1023.00 B"),
            (1024, "1.00 KB"),
            (1048576, "1.00 MB"),
            (1073741824, "1.00 GB"),
        ],
    )
    def test_converter_tamanho(self, bytes_entrada: int, resultado_esperado: str) -> None:
        """Testa conversão de tamanhos legíveis."""
        assert converter_tamanho(tamanho_bytes=bytes_entrada) == resultado_esperado

    def test_converter_tamanho_valor_negativo(self) -> None:
        """Testa conversão com valor negativo, espera ValueError."""
        with pytest.raises(expected_exception=ValueError):
            converter_tamanho(tamanho_bytes=-1)

    def test_coletar_permissoes(self) -> None:
        """Testa extração das permissões com todos os bits ativados."""
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o777  # permissões completas
        perms: PermissoesDetalhadas = coletar_permissoes(stats=mock_stat)
        for categoria in ["usuario", "grupo", "outros"]:
            assert perms[categoria]["ler"] is True
            assert perms[categoria]["escrever"] is True
            assert perms[categoria]["executar"] is True

    def test_coletar_tempos(self) -> None:
        """Testa conversão de tempos para datetime."""
        mock_stat = MagicMock()
        mock_stat.st_ctime = 1672531200
        mock_stat.st_mtime = 1672617600
        mock_stat.st_atime = 1672704000

        tempos: Tempos = coletar_tempos(stats=mock_stat)
        assert tempos.get("data_criacao") is not None
        assert tempos.get("data_modificacao") is not None
        assert tempos.get("data_acesso") is not None

    def test_coletar_info_basica_arquivo(self, tmp_path: Path) -> None:
        """Testa coleta de metadados básicos para arquivo."""
        file: Path = tmp_path / "teste.txt"
        file.write_text(data="conteudo")
        stats: stat_result = file.stat()
        info: MetadadosArquivo = coletar_info_basica(path=file, stats=stats)
        assert info.get("nome") == "teste.txt"
        assert info.get("tipo") == "arquivo"
        assert info.get("extensao") == ".txt"
        assert info.get("extensao_legivel") == "TXT"
        assert info.get("eh_oculto") is False

    def test_coletar_info_basica_pasta(self, tmp_path: Path) -> None:
        """Testa coleta de metadados básicos para diretório."""
        info: MetadadosArquivo = coletar_info_basica(path=tmp_path, stats=tmp_path.stat())
        assert info.get("nome") == tmp_path.name
        assert info.get("tipo") == "pasta"
        assert "extensao" not in info

    def test_gerar_dados_item_valido(self, tmp_path: Path) -> None:
        """Testa geração completa de metadados para arquivo válido."""
        file: Path = tmp_path / "exemplo.log"
        file.write_text(data="teste")
        dados: MetadadosArquivo = gerar_dados_item(caminho=file)
        assert dados.get("nome") == "exemplo.log"
        assert dados.get("tipo") == "arquivo"
        assert dados.get("extensao") == ".log"

    def test_gerar_dados_item_invalido(self) -> None:
        """Testa geração de metadados para caminho inválido, espera exceção."""
        with pytest.raises(expected_exception=ErroAcessoArquivo):
            gerar_dados_item(caminho="/caminho/inexistente")

    def test_erro_acesso_arquivo_str_repr(self) -> None:
        """Testa a representação string da exceção personalizada."""
        err = ErroAcessoArquivo(
            mensagem="Mensagem de erro",
            caminho="/caminho/teste",
            original=ValueError("orig"),
        )
        s = str(err)
        assert "Mensagem de erro" in s
        assert "/caminho/teste" in s
        assert "orig" in s


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
