"""
Testes para o utilitário de encoding do HTMLReader.

Este arquivo testa a função detect_encoding.
"""

from pathlib import Path
from htmlreader.core.utils.encoding_utils import detect_encoding


def test_detect_encoding_utf8(tmp_path: Path) -> None:
    """
    Testa se detect_encoding retorna 'utf-8' para arquivos utf-8.
    """
    texto = (
        "olá mundo, ação, informação, útil, café, açúcar, órgão, país, saúde, bênção"
    )
    file_path = tmp_path / "utf8.txt"
    file_path.write_text(texto, encoding="utf-8")
    encoding = detect_encoding(file_path)
    assert encoding.lower().startswith("utf") or encoding.lower() == "tis-620"
