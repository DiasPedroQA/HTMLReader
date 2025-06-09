import platform
import os
import sys


def obter_info_sistema() -> dict[str, str]:
    """
    Retorna informações básicas do sistema e ambiente Python.

    Returns:
        dict: Informações do sistema e da versão Python.
    """
    info = {
        "plataforma": platform.system(),
        "versao_plataforma": platform.version(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
    }
    return info


def eh_arquivo_html(caminho: str) -> bool:
    """Verifica se o caminho é um arquivo HTML válido."""
    return caminho.lower().endswith(".html") and os.path.isfile(caminho)


def eh_diretorio_valido(caminho: str) -> bool:
    """Verifica se o caminho é um diretório existente."""
    return os.path.isdir(caminho)
