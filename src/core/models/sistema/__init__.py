"""
Módulo central para modelos do sistema operacional.

Exporta:
    - SistemaInfo: Informações completas do ambiente
    - Utilitários de detecção do SO
    - Tipos compartilhados entre módulos
"""

from .sistema_info_model import SistemaInfo
from .sistema_operacional_model import SistemaOperacional, DadosSistemaOperacional
from .tipos_comuns_model import Permissoes, PermissoesDetalhadas, Tempos, MetadadosArquivo

__all__ = [
    "SistemaInfo", "SistemaOperacional", "DadosSistemaOperacional",
    "Permissoes", "PermissoesDetalhadas", "Tempos", "MetadadosArquivo"
]
