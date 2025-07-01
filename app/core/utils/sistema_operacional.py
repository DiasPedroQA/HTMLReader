"""
Módulo utilitário para detecção e coleta de informações do sistema operacional.

Este módulo fornece uma interface unificada para:
- Identificar o nome do sistema operacional atual
- Obter o caminho do diretório pessoal do usuário logado
- Verificar se o usuário atual possui privilégios de root (Unix-like)
- Confirmar a existência do caminho do usuário
- Tratar exceções e manter compatibilidade entre sistemas

Classes:
    - DadosSistemaOperacional: Contêiner de dados com informações do sistema.
    - SistemaOperacional: Classe utilitária com métodos estáticos de detecção.
"""

import os
import platform
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DadosSistemaOperacional:
    """
    Estrutura de dados que representa informações básicas do sistema operacional.

    Atributos:
        nome (str): Nome do sistema operacional (ex: 'linux', 'windows', 'darwin').
        caminho_usuario (Path): Caminho do diretório pessoal do usuário.
        usuario_root (bool): Indica se o usuário atual possui privilégios de root.
        encontrado (bool): Indica se o caminho do usuário foi encontrado com sucesso.
    """

    nome: str
    caminho_usuario: Path
    usuario_root: bool
    encontrado: bool


class SistemaOperacional:
    """
    Classe utilitária para operações relacionadas ao sistema operacional.
    """

    @staticmethod
    def detectar_nome() -> str:
        """
        Detecta o nome do sistema operacional atual de forma padronizada.

        Retorna:
            str: Nome em minúsculas do sistema operacional (e.g. 'linux', 'windows').
        """
        return platform.system().lower()

    @staticmethod
    def obter_dados_usuario() -> DadosSistemaOperacional:
        """
        Coleta os principais dados do ambiente do sistema operacional atual.

        Retorna:
            DadosSistemaOperacional: Objeto com dados padronizados e seguros sobre o SO.
        """
        nome_so: str = SistemaOperacional.detectar_nome()
        caminho: Path | None = None
        encontrado: bool = False
        usuario_root: bool = os.geteuid() == 0 if hasattr(os, "geteuid") else False

        try:
            if nome_so == "linux":
                caminho = Path.home()
            elif nome_so == "windows":
                caminho = Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
            elif nome_so == "darwin":
                caminho = Path.home()
            else:
                caminho = Path("/desconhecido")

            encontrado = caminho.exists()

        except OSError:
            caminho = Path("/erro")
            encontrado = False

        return DadosSistemaOperacional(
            nome=nome_so,
            caminho_usuario=caminho,
            usuario_root=usuario_root,
            encontrado=encontrado,
        )
