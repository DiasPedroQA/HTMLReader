"""
Testes unitários para a classe base `CaminhoBase`.

Valida:
- Identificação do retornar_o_tipo (arquivo, pasta, inexistente)
- Metadados: nome, existência, datas e tamanho
- Comportamento em arquivos e pastas temporários
"""

import tempfile
from datetime import datetime
from pathlib import Path

from core.models.model_caminho_base import CaminhoBase, TipoCaminho


class TestCaminhoBase:
    """Testes para a classe abstrata de caminhos `CaminhoBase`."""

    def test_para_arquivo_temporario(self) -> None:
        """Deve identificar corretamente um arquivo e seus metadados."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = Path(tmp.name)

        caminho = CaminhoBase(caminho=path)

        assert caminho.caminho_existe is True
        assert caminho.retornar_o_tipo == TipoCaminho.ARQUIVO
        assert caminho.nome_caminho == path.name
        assert caminho.caminho_absoluto == path
        assert isinstance(caminho.data_criacao, datetime)
        assert isinstance(caminho.data_modificacao, datetime)
        assert isinstance(caminho.tamanho_bytes, int)

        path.unlink()  # Remove o arquivo

    def test_para_diretorio_temporario(self) -> None:
        """Deve identificar corretamente um diretório e seus metadados básicos."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir)
            caminho = CaminhoBase(caminho=path)

            assert caminho.caminho_existe is True
            assert caminho.retornar_o_tipo == TipoCaminho.PASTA
            assert caminho.nome_caminho == path.name
            assert caminho.caminho_absoluto == path
            assert isinstance(caminho.tamanho_bytes, int | type(None))

    def test_para_caminho_inexistente(self) -> None:
        """Deve lidar corretamente com caminhos que não existem."""
        caminho_falso: Path = Path(tempfile.gettempdir()) / "caminho_inexistente_abcde.tmp"
        caminho = CaminhoBase(caminho=caminho_falso)

        assert caminho.caminho_existe is False
        assert caminho.retornar_o_tipo == TipoCaminho.DESCONHECIDO
        assert caminho.data_criacao is None
        assert caminho.data_modificacao is None
        assert caminho.tamanho_bytes is None
