"""
Testes para o serviço TextFileService do HTMLReader.

Foco: garantir leitura e escrita correta de palavras acentuadas.
"""

from pathlib import Path
from htmlreader.core.models.file_model import FileModel
from htmlreader.core.services.text_file_service import TextFileService


def test_read_write_accented(tmp_path: Path, monkeypatch) -> None:
    """
    Testa leitura e escrita de texto com acentuação, garantindo integridade dos caracteres.
    """
    texto = "Olá, ação, café, órgão, saúde, bênção"
    file_path = tmp_path / "acentuado.txt"
    file_path.write_text(texto, encoding="utf-8")
    file = FileModel(path=file_path)

    # Mock encoding para garantir leitura correta
    monkeypatch.setattr(
        "htmlreader.core.utils.encoding_utils.detect_encoding", lambda p: "utf-8"
    )

    # Leitura
    file_lido = TextFileService.read(file)
    assert file_lido.content == texto

    # Escrita
    destino = tmp_path / "saida.txt"
    TextFileService.write(file_lido, destino)
    assert destino.read_text(encoding="utf-8") == texto
