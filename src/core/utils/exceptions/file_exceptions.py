"""
Exceções personalizadas para operações com arquivos no sistema de arquivos.

Hierarquia de exceções:
- FileSystemError (base)
  - FileAccessError
    - CustomPermissionError
    - NotFoundError
  - FileOperationError
"""

from typing import Optional


class FileSystemError(Exception):
    """
    Exceção base para todos os erros relacionados ao sistema de arquivos.

    Args:
        message (str): Mensagem descritiva do erro.
        path (Optional[str]): Caminho do arquivo ou diretório relacionado ao erro.
    """

    def __init__(self, message: str, path: Optional[str] = None) -> None:
        self.path = path
        self.message = message
        full_message = f"{message} [Path: {path}]" if path else message
        super().__init__(full_message)


class FileAccessError(FileSystemError):
    """
    Exceção para erros de acesso a arquivos, incluindo permissões e existência.

    Args:
        message (str): Mensagem descritiva do erro.
        path (Optional[str]): Caminho do arquivo ou diretório.
        original_exc (Optional[Exception]): Exceção original capturada, se houver.
    """

    def __init__(
        self,
        message: str,
        path: Optional[str] = None,
        original_exc: Optional[Exception] = None,
    ) -> None:
        self.original_exc = original_exc
        full_message = f"Acesso negado: {message}"
        super().__init__(full_message, path)


class CustomPermissionError(FileAccessError):
    """
    Exceção para falhas específicas de permissão.

    Atributos:
        error_code (int): Código HTTP equivalente à permissão negada (403).
    """

    error_code: int = 403


class NotFoundError(FileAccessError):
    """
    Exceção para arquivo ou diretório não encontrado.

    Atributos:
        error_code (int): Código HTTP equivalente a recurso não encontrado (404).
    """

    error_code: int = 404


class FileOperationError(FileSystemError):
    """
    Exceção para erros durante operações de leitura, escrita ou manipulação de arquivos.

    Args:
        operation (str): Descrição da operação que falhou (ex: "leitura", "escrita").
        path (Optional[str]): Caminho do arquivo ou diretório.
        details (Optional[str]): Informações adicionais sobre a falha.
    """

    def __init__(
        self,
        operation: str,
        path: Optional[str] = None,
        details: Optional[str] = None,
    ) -> None:
        self.operation = operation
        self.details = details
        message = f"Falha na operação '{operation}'"
        if details:
            message += f": {details}"
        super().__init__(message, path)
