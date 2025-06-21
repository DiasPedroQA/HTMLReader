"""
Testes para a classe base de caminhos do sistema de arquivos.

Este módulo valida o comportamento da classe `CaminhoBase`, incluindo:
- Identificação de tipo de caminho (arquivo, pasta, inexistente)
- Recuperação de metadados (nome, existência, data, tamanho)
- Funcionamento em arquivos e pastas temporários
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime

from core.models.model_caminho_base import CaminhoBase, TipoCaminho


class TestCaminhoBase:
    """Classe de testes unitários para a `CaminhoBase`."""

    def test_atributos_para_arquivo_temporario(self) -> None:
        """
        Garante que um arquivo temporário é corretamente identificado como ARQUIVO
        e que seus metadados são acessíveis.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = Path(tmp.name)

        caminho = CaminhoBase(caminho=path)

        assert caminho.caminho_existe is True
        assert caminho.retornar_o_tipo == TipoCaminho.ARQUIVO
        assert caminho.nome_caminho == path.name
        assert caminho.caminho_absoluto == path
        assert isinstance(caminho.data_criacao, datetime)
        assert isinstance(caminho.data_modificacao, datetime)
        assert isinstance(caminho.tamanho_em_bytes, int)

        os.remove(path=path)

    def test_atributos_para_diretorio_temporario(self) -> None:
        """
        Garante que um diretório temporário é corretamente identificado como PASTA
        e que seus metadados básicos estão disponíveis.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir)
            caminho = CaminhoBase(caminho=path)

            assert caminho.caminho_existe is True
            assert caminho.retornar_o_tipo == TipoCaminho.PASTA
            assert caminho.nome_caminho == path.name
            assert caminho.caminho_absoluto == path
            assert caminho.tamanho_em_bytes is not None

    def test_caminho_inexistente(self) -> None:
        """
        Verifica que um caminho inexistente seja tratado corretamente como DESCONHECIDO
        e sem dados de metadados disponíveis.
        """
        caminho_falso: Path = Path(tempfile.gettempdir()) / "caminho_inexistente_abcde.tmp"
        caminho = CaminhoBase(caminho=caminho_falso)

        assert caminho.caminho_existe is False
        assert caminho.retornar_o_tipo == TipoCaminho.DESCONHECIDO
        assert caminho.data_criacao is None
        assert caminho.data_modificacao is None
        assert caminho.tamanho_em_bytes is None
