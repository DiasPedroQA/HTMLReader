"""
Tipos específicos para manipulação de arquivos.

Define estruturas de dados especializadas para operações com arquivos.
"""

from typing import TypedDict


class DadosConteudo(TypedDict):
    """Estrutura para representar conteúdo processado de arquivos."""

    texto: str
    encoding: str
    linhas: int
    palavras: int


class ResultadoLeitura(TypedDict):
    """Resultado padronizado de operações de leitura."""

    sucesso: bool
    conteudo: str
    bytes_lidos: int
    tempo_processamento: float


class FiltroArquivo(TypedDict, total=False):
    """Critérios para filtragem de arquivos."""

    extensoes: list[str]
    tamanho_min: int
    tamanho_max: int
    contem_texto: str
    modificado_apos: float  # Timestamp


class ErroAcessoArquivo(TypedDict, Exception, total=False):
    """Exceção personalizada para erros de acesso a arquivos."""

    mensagem: str
    caminho: str
