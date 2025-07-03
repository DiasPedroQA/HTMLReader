"""
Módulo de modelos para manipulação de arquivos.

Exporta:
    - Arquivo: Classe principal para representação de arquivos
    - Tipos especializados para operações com arquivos
    - Erros personalizados relacionados
"""

from .arquivo_model import Arquivo
from .tipos_model import DadosConteudo, ResultadoLeitura, FiltroArquivo

__all__ = ["Arquivo", "DadosConteudo", "ResultadoLeitura", "FiltroArquivo"]
