"""
Utilitários para detecção de encoding no HTMLReader.

Este módulo fornece função para detectar a codificação de arquivos.
"""

from pathlib import Path
from chardet import detect


def detect_encoding(path: Path) -> str:
    """
    Detecta a codificação de um arquivo usando chardet.

    Args:
        path (Path): Caminho do arquivo a ser analisado.

    Returns:
        str: Nome da codificação detectada, ou 'utf-8' se não detectado.
    """
    with path.open("rb") as file:
        raw = file.read(1024)
    result = detect(raw)
    return result["encoding"] or "utf-8"
