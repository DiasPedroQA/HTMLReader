"""
Testes para o modelo FileModel do HTMLReader.

Este arquivo testa a inicialização e validação do FileModel.
"""

from pathlib import Path
import pytest
from htmlreader.core.models.file_model import FileModel


def test_file_model_init(tmp_path: Path) -> None:
    """
    Testa a inicialização do FileModel com um arquivo existente.
    """
    file_path = tmp_path / "teste.txt"
    file_path.write_text("abc")
    model = FileModel(path=file_path)
    assert model.path == file_path
    assert model.encoding == "utf-8"
    assert model.content is None


def test_file_model_file_not_found(tmp_path: Path) -> None:
    """
    Testa se FileModel lança FileNotFoundError para arquivo inexistente.
    """
    with pytest.raises(FileNotFoundError):
        FileModel(path=tmp_path / "nao_existe.txt")


def test_file_model_not_a_file(tmp_path: Path) -> None:
    """
    Testa se FileModel lança ValueError quando o caminho não é um arquivo.
    """
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    with pytest.raises(ValueError):
        FileModel(path=dir_path)
