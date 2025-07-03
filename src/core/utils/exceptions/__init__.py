"""
Pacote de exceções personalizadas para o sistema de arquivos.

Exporta as exceções para tratamento uniforme em toda a aplicação.
"""

from .file_exceptions import (
    FileSystemError,
    FileAccessError,
    CustomPermissionError,
    NotFoundError,
    FileOperationError,
)

__all__ = [
    "FileSystemError",
    "FileAccessError",
    "CustomPermissionError",
    "NotFoundError",
    "FileOperationError",
]
