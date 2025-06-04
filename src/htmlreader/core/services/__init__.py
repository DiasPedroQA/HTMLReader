"""
Pacote de serviços do HTMLReader.

Importa e expõe os principais serviços para facilitar o acesso em outros módulos.
"""
from .processador_service import processar_arquivo, processar_em_lote
from .visor_service import listar_conteudo, obter_previa

__all__ = [
    "listar_conteudo",
    "obter_previa",
    "processar_arquivo",
    "processar_em_lote",
]
