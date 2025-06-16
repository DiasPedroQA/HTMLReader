"""
Utilitários para obtenção de informações do sistema operacional,
validação de caminhos e manipulação básica de arquivos e diretórios.
"""

from getpass import getuser
from pathlib import Path
from platform import system


def obter_info_sistema(nome_forcado: str | None = None) -> str:
    """Obtém o nome do sistema operacional atual ou simulado.

    Args:
        nome_forcado: Nome do SO para simulação (opcional)

    Returns:
        Nome do sistema operacional em minúsculas
    """
    return nome_forcado.lower() if nome_forcado else system().lower()


def obter_diretorio_usuario(nome_sistema: str | None = None) -> Path | None:
    """Obtém o caminho da pasta home do usuário para o SO especificado.

    Args:
        nome_sistema: Nome do SO ('linux', 'windows' ou 'darwin')

    Returns:
        Objeto Path do diretório home ou None se não existir

    Raises:
        OSError: Se o SO não for suportado
    """
    sistema_atual: str = obter_info_sistema(nome_forcado=nome_sistema)
    usuario = getuser()

    caminhos = {
        "windows": f"C:/Users/{usuario}",
        "linux": f"/home/{usuario}",
        "darwin": f"/Users/{usuario}",
        "mac": f"/Users/{usuario}",
    }

    if sistema_atual not in caminhos:
        raise OSError(f"Sistema operacional não suportado: {sistema_atual}")

    caminho = Path(caminhos.get(sistema_atual, f"/home/{usuario}"))
    return caminho if caminho.exists() else None


def validar_caminho(caminho: str) -> Path | None:
    """Verifica se um caminho existe e retorna como objeto Path.

    Args:
        caminho: Caminho a ser validado

    Returns:
        Objeto Path se existir, None caso contrário
    """
    objeto_caminho = Path(caminho)
    return objeto_caminho if objeto_caminho.exists() else None
