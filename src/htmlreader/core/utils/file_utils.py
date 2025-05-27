"""
Utilitários para manipulação de arquivos no HTMLReader.

Este módulo fornece funções para verificar tipos de arquivos e ler arquivos em modo binário.
"""

from pathlib import Path


def is_text_file(path: Path) -> bool:
    """
    Verifica se o arquivo fornecido é um arquivo de texto suportado.

    Args:
        path (Path): Caminho para o arquivo.

    Returns:
        bool: True se o arquivo for .txt, .md ou .html, caso contrário False.
    """
    return path.suffix.lower() in [".txt", ".md", ".html"]
