"""
Testes automatizados para o módulo de utilitários de formatação de arquivos e diretórios.

Este conjunto de testes cobre:
- Extração de metadados com `gerar_dados_item`
- Conversão legível de tamanhos com `converter_tamanho`
- Verificação de permissões e tipos de caminho
- Tratamento de erros com `ErroAcessoArquivo`
"""

from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from src.core.utils.formatadores import (
    ErroAcessoArquivo,
    MetadadosArquivo,
    PermissoesDetalhadas,
    converter_tamanho,
    gerar_dados_item,
)


class TestFormatadoresUtilitarios:
    """
    Classe de testes unitários para funções do módulo `formatadores.py`.

    Cada método testa funcionalidades específicas relacionadas à leitura e
    formatação de metadados de arquivos e diretórios, bem como validações e exceções.
    """

    def test_gerar_dados_de_arquivo_valido(self) -> None:
        """
        Garante que a função `gerar_dados_item` retorna metadados corretos para um arquivo válido.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"conteudo de teste")
            tmp_path = Path(tmp.name)

        dados: MetadadosArquivo = gerar_dados_item(caminho=tmp_path)

        assert dados.get("nome") == tmp_path.name
        assert dados.get("tamanho_bytes") == tmp_path.stat().st_size
        assert dados.get("tipo") == "arquivo"
        assert dados.get("extensao") == tmp_path.suffix.lower()
        assert dados.get("caminho_absoluto") == str(tmp_path.absolute())
        assert isinstance(dados.get("data_criacao"), datetime)

        tmp_path.unlink()

    def test_gerar_dados_de_diretorio_valido(self) -> None:
        """
        Verifica que `gerar_dados_item` funciona corretamente com diretórios.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir)
            dados: MetadadosArquivo = gerar_dados_item(caminho=path)

            assert dados.get("tipo") == "pasta"
            assert dados.get("nome") == path.name
            assert dados.get("caminho_absoluto") == str(path.absolute())

    def test_caminho_inexistente_lanca_erro(self) -> None:
        """
        Garante que a função levanta `ErroAcessoArquivo` para caminhos inválidos.
        """
        caminho = "/caminho/inexistente/arquivo.txt"
        with pytest.raises(expected_exception=ErroAcessoArquivo):
            gerar_dados_item(caminho=caminho)

    def test_converter_tamanho_valores_diferentes(self) -> None:
        """
        Valida conversão correta de diversos tamanhos em bytes para formato legível.
        """
        assert converter_tamanho(tamanho_bytes=0) == "0.00 B"
        assert converter_tamanho(tamanho_bytes=1023) == "1023.00 B"
        assert converter_tamanho(tamanho_bytes=1024) == "1.00 KB"
        assert converter_tamanho(tamanho_bytes=1536) == "1.50 KB"
        assert converter_tamanho(tamanho_bytes=1048576) == "1.00 MB"

    # def test_tipo_invalido_para_caminho(self) -> None:
    #     """
    #     Testa se `TypeError` é levantado ao passar tipo não suportado como caminho.
    #     """
    #     with pytest.raises(expected_exception=TypeError):
    #         gerar_dados_item(caminho="1234")

    # def test_converter_tamanho_valor_invalido(self) -> None:
    #     """
    #     Verifica que `converter_tamanho` levanta erro para valores negativos ou absurdos.
    #     """
    #     with pytest.raises(expected_exception=ValueError):
    #         converter_tamanho(tamanho_bytes=-10)
    #     with pytest.raises(expected_exception=ValueError):
    #         converter_tamanho(tamanho_bytes=6.022e23)

    def test_permissoes_arquivo(self) -> None:
        """
        Testa se as permissões retornadas estão corretas após modificar o modo de um arquivo.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
        tmp_path.chmod(mode=0o764)
        dados: MetadadosArquivo = gerar_dados_item(caminho=tmp_path)

        permissoes: PermissoesDetalhadas | dict = dados.get("permissoes", {})
        assert permissoes.get("usuario", {}).get("ler") is True
        assert permissoes.get("usuario", {}).get("escrever") is True
        assert permissoes.get("usuario", {}).get("executar") is True

        assert permissoes.get("grupo", {}).get("ler") is True
        assert permissoes.get("grupo", {}).get("escrever") is True
        assert permissoes.get("grupo", {}).get("executar") is False

        assert permissoes.get("outros", {}).get("ler") is True
        assert permissoes.get("outros", {}).get("escrever") is False
        assert permissoes.get("outros", {}).get("executar") is False

        tmp_path.unlink()

    def test_excecao_erro_acesso_arquivo_customizada(self) -> None:
        """
        Garante que a exceção `ErroAcessoArquivo` exibe a mensagem formatada corretamente.
        """
        erro = ErroAcessoArquivo(
            mensagem="Falha ao acessar",
            caminho="/algum/caminho",
            original=OSError("Permissão negada"),
        )
        msg = str(erro)
        assert "Falha ao acessar" in msg
        assert "/algum/caminho" in msg
        assert "Permissão negada" in msg
