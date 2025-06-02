"""
Exceções customizadas para o HTMLReader.

Define erros específicos para manipulação e processamento de arquivos e caminhos.
"""


class CaminhoInvalidoError(Exception):
    """
    Exceção para indicar que um caminho fornecido é inválido.
    """


class ArquivoNaoSuportadoError(Exception):
    """
    Exceção para indicar que o arquivo fornecido não é suportado pelo sistema.
    """


class ErroDeProcessamento(Exception):
    """
    Exceção para indicar erro durante o processamento de arquivos.
    """
