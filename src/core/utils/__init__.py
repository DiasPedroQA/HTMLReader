"""
Módulo de utilitários do sistema.

Exporta:
    - filesystem: Operações com arquivos
    - exceptions: Exceções personalizadas
    - loggers: Configuração de logging
"""

import logging


from src.core.utils.exceptions.file_exceptions import FileAccessError
from src.core.utils.filesystem.detectores import sistema_operacional
from src.core.utils.filesystem.metadados import coletor_metadados
from src.core.utils.filesystem.metadados import coletor_permissoes
from src.core.utils.filesystem.metadados import coletor_tempos


__all__ = [
    # Re-exportações principais
    "FileAccessError",
    # Módulos completos
    "sistema_operacional",
    "coletor_metadados",
    "coletor_permissoes",
    "coletor_tempos",
]

# Configuração básica de logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
