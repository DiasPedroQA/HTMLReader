"""
Testes para o módulo path_utils do HTMLReader.

Este arquivo testa as funções normalize_path e ensure_dir.
"""

from pathlib import Path
from htmlreader.core.utils.path_utils import normalize_path, ensure_dir


def test_normalize_path(tmp_path: Path) -> None:
    """
    Testa se normalize_path retorna um objeto Path absoluto.
    """
    p = normalize_path(str(tmp_path / "pasta"))
    assert isinstance(p, Path)
    assert p.is_absolute()


def test_ensure_dir(tmp_path: Path) -> None:
    """
    Testa se ensure_dir cria o diretório se ele não existir.
    """
    dir_path = tmp_path / "novo_dir"
    assert not dir_path.exists()
    ensure_dir(dir_path)
    assert dir_path.exists()
    assert dir_path.is_dir()
