"""
Modelo para manipulação de diretórios no HTMLReader.

Este módulo define a classe DirectoryModel para listar arquivos em um diretório.
"""

from pathlib import Path
from typing import List
from .file_model import FileModel


class DirectoryModel:
    """
    Representa um diretório e permite listar seus arquivos.
    """

    def __init__(self, path: Path) -> None:
        """
        Inicializa o modelo de diretório.

        Args:
            path (Path): Caminho do diretório.
        """
        self.path: Path = path
        self.files: List[FileModel] = []

    def list_files(self, pattern: str = "*") -> List[FileModel]:
        """
        Lista os arquivos do diretório que correspondem ao padrão fornecido.

        Args:
            pattern (str, opcional): Padrão de busca dos arquivos (default: "*").

        Returns:
            List[FileModel]: Lista de objetos FileModel para os arquivos encontrados.
        """
        self.files = [FileModel(p) for p in self.path.glob(pattern) if p.is_file()]
        return self.files

    def count_files(self, pattern: str = "*") -> int:
        """
        Conta o número de arquivos no diretório que correspondem ao padrão fornecido.

        Args:
            pattern (str, opcional): Padrão de busca dos arquivos (default: "*").

        Returns:
            int: Número de arquivos encontrados.
        """
        return len([p for p in self.path.glob(pattern) if p.is_file()])
