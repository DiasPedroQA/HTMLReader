"""
Utilitários para manipulação e normalização de caminhos no HTMLReader.

Este módulo fornece funções para normalizar caminhos e garantir a existência de diretórios.
"""

from pathlib import Path


def normalize_path(path: str) -> Path:
    """
    Normaliza um caminho, expandindo o usuário e resolvendo para um caminho absoluto.

    Args:
        path (str): Caminho a ser normalizado.

    Returns:
        Path: Caminho normalizado como objeto Path.
    """
    p = Path(path)
    return p.expanduser().resolve()


def ensure_dir(path: Path) -> None:
    """
    Garante que o diretório especificado exista, criando-o se necessário.

    Args:
        path (Path): Caminho do diretório a ser garantido.

    Returns:
        None
    """
    if not path.exists():
        path.mkdir(parents=True)
