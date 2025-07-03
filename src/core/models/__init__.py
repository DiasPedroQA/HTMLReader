"""
Módulo central de modelos do sistema.

Exporta todos os modelos organizados por categoria:

1. Sistema: Modelos relacionados ao sistema operacional
2. Arquivo: Modelos para manipulação de arquivos
3. Pasta: Modelos para manipulação de diretórios

Usage:
    >>> from core.models import SistemaInfo, Arquivo, Pasta
    >>> from core.models.sistema import SistemaOperacional
"""

# Inicialização do sistema de logging
import logging

# Re-exportações principais
from .sistema.sistema_info_model import SistemaInfo
from .sistema.sistema_operacional_model import SistemaOperacional
from .arquivo.arquivo_model import Arquivo
from .pasta.pasta_model import Pasta

# Tipos comuns para importação direta
from .sistema.tipos_comuns_model import MetadadosArquivo, Permissoes, PermissoesDetalhadas, Tempos

__all__ = [
    # Classes principais
    "SistemaInfo",
    "SistemaOperacional",
    "Arquivo",
    "Pasta",
    # Tipos compartilhados
    "MetadadosArquivo",
    "Permissoes",
    "PermissoesDetalhadas",
    "Tempos",
]


logging.getLogger(__name__).addHandler(logging.NullHandler())
