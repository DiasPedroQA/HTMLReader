"""
Pacote de metadados do sistema de arquivos.

Exporta as funções principais para coleta e processamento de metadados.
"""

from .coletor_permissoes import coletar_permissoes
from .coletor_tempos import coletar_tempos
from .gerador_metadados import gerar_dados_item

__all__ = [
    "gerar_dados_item",
    "coletar_permissoes",
    "coletar_tempos",
]
