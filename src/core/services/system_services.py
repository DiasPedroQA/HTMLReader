"""
Utilitários para obtenção de informações do sistema operacional.

Fornece classes e métodos para:
- Detecção do sistema operacional
- Obtenção de caminhos padrão do usuário
- Validação e manipulação básica de arquivos e diretórios

O módulo foi otimizado para Python 3.12+, utilizando:
- Type hints específicos da versão
- Pattern matching (match/case)
- Enumerações modernas
- Operações de sistema otimizadas

Classes:
    SistemaOperacional: Enumeração que representa sistemas operacionais suportados
        com métodos para detecção e operações relacionadas.
"""

from getpass import getuser
from pathlib import Path
from platform import system
from enum import Enum
from typing import Optional


class SistemaOperacional(str, Enum):
    """Enumeração dos sistemas operacionais suportados pelo módulo.

    Atributos:
        WINDOWS: Representa o sistema operacional Windows
        LINUX: Representa sistemas baseados em Linux
        MACOS: Representa o sistema operacional macOS
    """

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"

    @classmethod
    def detectar(cls, sistema_simulado: Optional[str] = None) -> "SistemaOperacional":
        """Detecta o sistema operacional em execução.

        Args:
            sistema_simulado: Opcional. Permite simular um sistema para testes.
                Se None, detecta o sistema real.

        Returns:
            SistemaOperacional: Enumeração correspondente ao sistema detectado.

        Raises:
            ValueError: Se o sistema detectado não for suportado.

        Exemplos:
            >>> SistemaOperacional.detectar()
            <SistemaOperacional.LINUX: 'linux'>

            >>> SistemaOperacional.detectar("Windows 11")
            <SistemaOperacional.WINDOWS: 'windows'>
        """
        nome_bruto: str = (sistema_simulado or system()).casefold()
        nome: str = nome_bruto.split(".")[-1]  # Pega o último segmento após ponto

        sistemas_permitidos: dict[str, "SistemaOperacional"] = {
            "windows": cls.WINDOWS,
            "win32": cls.WINDOWS,
            "linux": cls.LINUX,
            "darwin": cls.MACOS,
            "mac": cls.MACOS,
            "macos": cls.MACOS,
        }

        for key, value in sistemas_permitidos.items():
            if key in nome:
                return value

        raise ValueError(f"Sistema não suportado: {nome_bruto} (processado: {nome})")

    @classmethod
    def obter_raiz_usuario(cls, sistema_desejado: Optional[str] = None) -> Path:
        """Obtém o caminho raiz do diretório do usuário para o sistema especificado.

        Args:
            sistema_desejado: Opcional. Nome do sistema para o qual obter o caminho.
                Se None, usa o sistema atual.

        Returns:
            Path: Objeto Path apontando para o diretório home do usuário.

        Raises:
            ValueError: Se o sistema especificado não for suportado.

        Exemplos:
            >>> SistemaOperacional.obter_raiz_usuario()
            PosixPath('/home/usuario')

            >>> SistemaOperacional.obter_raiz_usuario("windows")
            WindowsPath('C:/Users/usuario')
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
            case _:
                raise ValueError(f"Sem suporte para sistema: {sistema}")

    @staticmethod
    def _raise_unsupported_system(nome: str) -> None:
        """Método interno para lançar exceção de sistema não suportado.

        Args:
            nome: Nome do sistema não suportado.

        Raises:
            ValueError: Sempre que chamado, com mensagem formatada.
        """
        raise ValueError(f"Sistema operacional não suportado ou desconhecido: {nome}")
