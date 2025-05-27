"""
Utilitários para informações do sistema operacional e análise de caminhos no HTMLReader.
"""

import platform

from .encoding_utils import detect_encoding
from .file_utils import is_text_file
from .path_utils import ensure_dir, normalize_path


def get_os_info() -> dict[str, str]:
    """
    Obtém informações do sistema operacional.

    Returns:
        dict[str, str]: Dicionário com informações do sistema operacional.
    """
    return {
        "Sistema": platform.system(),
        "Versão": platform.version(),
        "Arquitetura": platform.architecture()[0],
        "Processador": platform.processor(),
        "Nome da máquina": platform.node(),
        "Release": platform.release(),
        "Plataforma": platform.platform(),
    }


def analyze_path(path: str) -> dict[str, str]:
    """
    Analisa um caminho de arquivo ou diretório.

    Args:
        path (str): Caminho do arquivo ou diretório a ser analisado.

    Returns:
        dict[str, str]: Dicionário com informações sobre o caminho.
    """
    p = normalize_path(path)
    ensure_dir(p.parent)

    if not p.exists():
        return {"Erro": "Caminho não existe"}

    return {
        "Caminho Absoluto": str(p.resolve()),
        "É Diretório": "Sim" if p.is_dir() else "Não",
        "É Arquivo": "Sim" if p.is_file() else "Não",
        "Tamanho (bytes)": str(p.stat().st_size),
        "É Texto": "Sim" if is_text_file(p) else "Não",
        "Codificação": detect_encoding(p) if is_text_file(p) else "N/A",
    }
