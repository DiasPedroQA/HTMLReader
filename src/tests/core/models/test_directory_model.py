"""
Testes para o modelo DirectoryModel do HTMLReader.

Este arquivo testa a inicialização, listagem e contagem de arquivos do diretório.
"""

from pathlib import Path
from htmlreader.core.models.directory_model import DirectoryModel
from htmlreader.core.models.file_model import FileModel


def test_directory_model_init(tmp_path: Path) -> None:
    """
    Testa a inicialização do DirectoryModel.
    """
    dir_model = DirectoryModel(tmp_path)
    assert dir_model.path == tmp_path
    assert dir_model.files == []


def test_list_files(tmp_path: Path) -> None:
    """
    Testa se list_files retorna corretamente os arquivos do diretório.
    """
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.md"
    file1.write_text("abc")
    file2.write_text("def")
    dir_model = DirectoryModel(tmp_path)
    files = dir_model.list_files("*.txt")
    assert isinstance(files, list)
    assert all(isinstance(f, FileModel) for f in files)
    assert len(files) == 1
    assert files[0].path == file1


def test_count_files(tmp_path: Path) -> None:
    """
    Testa se count_files retorna corretamente o número de arquivos do diretório.
    """
    (tmp_path / "a.txt").write_text("abc")
    (tmp_path / "b.md").write_text("def")
    (tmp_path / "c.png").write_bytes(b"bin")
    dir_model = DirectoryModel(tmp_path)
    assert dir_model.count_files("*.txt") == 1
    assert dir_model.count_files("*.md") == 1
    assert dir_model.count_files("*") == 3
