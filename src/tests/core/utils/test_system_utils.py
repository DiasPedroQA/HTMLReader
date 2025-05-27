"""
Testes para os utilitários de sistema e análise de caminhos do HTMLReader.
"""

from pathlib import Path
from htmlreader.core.utils.system_utils import get_os_info, analyze_path


def test_get_os_info() -> None:
    """
    Testa se get_os_info retorna um dicionário com chaves esperadas.
    """
    info = get_os_info()
    assert isinstance(info, dict)
    assert "Sistema" in info
    assert "Versão" in info


def test_analyze_path_file(tmp_path: Path) -> None:
    """
    Testa analyze_path para um arquivo existente.
    """
    file_path = tmp_path / "teste.txt"
    file_path.write_text("abc", encoding="utf-8")
    result = analyze_path(str(file_path))
    assert result["É Arquivo"] is True
    assert result["É Diretório"] is False
    assert result["Tamanho (bytes)"] == 3
    assert result["É Texto"] is True
    assert result["Codificação"].lower().startswith("utf")


def test_analyze_path_dir(tmp_path: Path) -> None:
    """
    Testa analyze_path para um diretório existente.
    """
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    result = analyze_path(str(dir_path))
    assert result["É Diretório"] is True
    assert result["É Arquivo"] is False


def test_analyze_path_not_exists(tmp_path: Path) -> None:
    """
    Testa analyze_path para um caminho inexistente.
    """
    fake_path = tmp_path / "nao_existe.txt"
    result = analyze_path(str(fake_path))
    assert "Erro" in result
