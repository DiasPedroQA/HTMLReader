"""
Utilitários para detecção do ambiente do sistema operacional.

Classes:
    DadosSistemaOperacional: Contêiner para dados do SO
    SistemaOperacional: Métodos estáticos para detecção
"""

import os
import platform
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Literal

from .sistema_info_model import SistemaInfo


@dataclass
class DadosSistemaOperacional:
    """
    Dados básicos do sistema operacional atual.

    Atributos:
        nome: Nome normalizado do SO ('linux', 'windows', 'darwin')
        caminho_usuario: Path do diretório home
        usuario_root: Bool indicando privilégios elevados
        timestamp: Momento da coleta
    """

    nome: Literal["linux", "windows", "darwin", "outro"]
    caminho_usuario: Path
    usuario_root: bool
    timestamp: float = field(default_factory=time.time)


class SistemaOperacional:
    """Métodos utilitários para interação com o SO."""

    @staticmethod
    def detectar() -> DadosSistemaOperacional:
        """Detecta automaticamente as configurações do SO."""
        so_map = {"Linux": "linux", "Windows": "windows", "Darwin": "darwin"}
        nome = so_map.get(platform.system(), "outro")

        return DadosSistemaOperacional(
            nome=nome,
            caminho_usuario=Path.home(),
            usuario_root=os.geteuid() == 0 if hasattr(os, "geteuid") else False,
        )

    @staticmethod
    def criar_sistema_info() -> SistemaInfo:
        """Gera um objeto SistemaInfo com dados atualizados."""
        dados = SistemaOperacional.detectar()
        return SistemaInfo(
            sistema_operacional=platform.system(),
            versao=platform.release(),
            arquitetura=platform.machine(),
            nome_maquina=platform.node(),
            tempo_atividade=time.monotonic(),
            diretorio_atual=str(Path.cwd()),
            usuario=os.getlogin(),
            permissoes="root" if dados.usuario_root else "padrão",
        )
