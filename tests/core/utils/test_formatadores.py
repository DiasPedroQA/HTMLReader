"""
Testes automatizados para o módulo de utilitários de formatação de arquivos e diretórios.

Este conjunto de testes cobre:
- Extração de metadados com `gerar_dados_item`
- Conversão legível de tamanhos com `converter_tamanho`
- Verificação de permissões e tipos de caminho
- Tratamento de erros com `ErroAcessoArquivo`
"""

from __future__ import annotations

from os import stat_result
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.core.utils.formatadores import (
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
    """Testes para funções do módulo formatadores."""

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
