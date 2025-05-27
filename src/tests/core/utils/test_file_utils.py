"""
Testes para o módulo file_utils do HTMLReader.

Este arquivo testa as funções is_text_file e read_binary.
"""

from pathlib import Path
from htmlreader.core.utils.file_utils import is_text_file, read_binary


def test_is_text_file_true(tmp_path: Path) -> None:
    """
    Testa se is_text_file retorna True para arquivos de texto suportados.
    """
    for ext in [".txt", ".md", ".html"]:
        file = tmp_path / f"arquivo{ext}"
        file.write_text("teste")
        assert is_text_file(file) is True


def test_is_text_file_false(tmp_path: Path) -> None:
    """
    Testa se is_text_file retorna False para arquivos não suportados.
    """
    for ext in [".pdf", ".png", ".exe"]:
        file = tmp_path / f"arquivo{ext}"
        file.write_bytes(b"binario")
        assert is_text_file(file) is False


def test_read_binary(tmp_path: Path) -> None:
    """
    Testa se read_binary retorna corretamente o conteúdo binário do arquivo.
    """
    file = tmp_path / "arquivo.bin"
    data = b"conteudo binario"
    file.write_bytes(data)
    assert read_binary(file) == data
