"""
Pacote de modelos (schemas) do HTMLReader.

Importa e expõe os principais modelos para facilitar o acesso em outros módulos.
"""
from .processador_models import (
    ArquivoNaoSuportadoError,
    CaminhoArquivo,
    CaminhoInvalidoError,
    ErroDeProcessamento,
    LoteDeArquivos,
    ResultadoProcessamento,
)
from .visor_models import CaminhoEntrada, FiltroVisor, ItemDePasta, ListaDeItens, PreviaArquivo

__all__ = [
    "CaminhoEntrada",
    "FiltroVisor",
    "ItemDePasta",
    "ListaDeItens",
    "PreviaArquivo",
    "CaminhoArquivo",
    "ResultadoProcessamento",
    "LoteDeArquivos",
    "CaminhoInvalidoError",
    "ArquivoNaoSuportadoError",
    "ErroDeProcessamento",
]
