"""
Pacote principal para operações relacionadas ao sistema de arquivos.

Exporta:
    - detectores: Módulo para detecção de ambiente do sistema operacional
    - metadados: Módulo para coleta e processamento de metadados de arquivos e diretórios
"""


from . import detectores
from . import metadados

__all__ = [
    "detectores",
    "metadados",
]
