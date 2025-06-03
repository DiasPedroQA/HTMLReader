"""
Pacote de modelos (schemas) do HTMLReader.

Importa e expõe os principais modelos para facilitar o acesso em outros módulos.
"""

from .visor_models import (
    CaminhoEntrada,
    FiltroVisor,
    ItemDePasta,
    ListaDeItens,
    PreviaArquivo,
)
from .processador_models import (
    CaminhoArquivo,
    ResultadoProcessamento,
    LoteDeArquivos,
    CaminhoInvalidoError,
    ArquivoNaoSuportadoError,
    ErroDeProcessamento,
)

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
