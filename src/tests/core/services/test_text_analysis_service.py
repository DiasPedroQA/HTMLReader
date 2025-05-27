"""
Testes para o serviço TextAnalysisService do HTMLReader.

Este arquivo testa as funções de contagem de palavras e linhas, e a contagem em lote.
"""

from pathlib import Path
from htmlreader.core.models.file_model import FileModel
from htmlreader.core.models.directory_model import DirectoryModel
from htmlreader.core.services.text_analysis_service import TextAnalysisService


def test_count_words() -> None:
    """
    Testa a contagem de palavras em um arquivo.
    """
    file = FileModel(path=Path("README.md"))
    file.content = "uma duas três quatro"
    assert TextAnalysisService.count_words(file) == 4


def test_count_lines() -> None:
    """
    Testa a contagem de linhas em um arquivo.
    """
    file = FileModel(path=Path("README.md"))
    file.content = "linha1\nlinha2\nlinha3"
    assert TextAnalysisService.count_lines(file) == 3


def test_batch_count_words(tmp_path: Path) -> None:
    """
    Testa a contagem de palavras em lote para arquivos de um diretório.
    """
    # Cria arquivos reais para FileModel
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("um dois tres")
    file2.write_text("quatro cinco")
    f1 = FileModel(path=file1)
    f1.content = file1.read_text()
    f2 = FileModel(path=file2)
    f2.content = file2.read_text()
    dir_model = DirectoryModel(tmp_path)
    dir_model.files = [f1, f2]
    result = TextAnalysisService.batch_count_words(dir_model)
    assert result == {"a.txt": 3, "b.txt": 2}
