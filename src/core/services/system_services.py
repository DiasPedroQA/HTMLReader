"""
Utilitários para obtenção de informações do sistema operacional,
validação de caminhos e manipulação básica de arquivos e diretórios.

Módulo otimizado para Python 3.12, utilizando type hints mais recentes
e recursos de performance específicos desta versão.
"""

from getpass import getuser
from pathlib import Path
from platform import system
from enum import Enum


class SistemaOperacional(str, Enum):
    """Enum para representar sistemas operacionais suportados."""

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"

    @classmethod
    def detectar(cls, sistema_simulado: str | None = None) -> "SistemaOperacional":
        """Detecta ou valida um nome de sistema operacional conhecido.

        Args:
            sistema_simulado (str | None): Nome do sistema para simular (ou None para autodetecção).

        Returns:
            SistemaOperacional: Valor correspondente da enumeração.

        Raises:
            ValueError: Se o nome não for reconhecido.
        """
        nome: str = (sistema_simulado or system()).casefold()
        sistemas_permitidos: dict[str, SistemaOperacional] = {
            "windows": cls.WINDOWS,
            "win32": cls.WINDOWS,
            "linux": cls.LINUX,
            "darwin": cls.MACOS,
            "mac": cls.MACOS,
            "macos": cls.MACOS,
        }

        if nome in sistemas_permitidos:
            return sistemas_permitidos[nome]

        raise ValueError(f"Sistema operacional não suportado ou desconhecido: {nome}")

    @classmethod
    def obter_raiz_usuario(cls, sistema_desejado: str | None = None) -> Path:
        """Retorna o caminho base da pasta pessoal do usuário.

        Args:
            sistema_desejado (str | None): Nome opcional do sistema a simular.

        Returns:
            Path: Caminho da pasta pessoal do usuário.

        Raises:
            ValueError: Se o sistema informado não for suportado.
        """
        sistema: SistemaOperacional = cls.detectar(sistema_simulado=sistema_desejado)
        nome_usuario: str = getuser()

        match sistema:
            case cls.WINDOWS:
                return Path(f"C:/Users/{nome_usuario}")
            case cls.LINUX:
                return Path(f"/home/{nome_usuario}")
            case cls.MACOS:
                return Path(f"/Users/{nome_usuario}")
            case _:  # segurança extra
                raise ValueError(f"Sem suporte para sistema: {sistema}")
