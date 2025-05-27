"""
Modelo para manipulação de arquivos no HTMLReader.

Este módulo define a classe FileModel para representar arquivos individuais.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FileModel:
    """
    Representa um arquivo individual.

    Attributes:
        path (Path): Caminho do arquivo.
        encoding (str): Codificação do arquivo.
        content (Optional[str]): Conteúdo do arquivo (pode ser None).
    """

    path: Path
    encoding: str = "utf-8"
    content: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """
        Valida se o caminho existe e é um arquivo.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ValueError: Se o caminho não for um arquivo.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.path}")
        if not self.path.is_file():
            raise ValueError(f"Não é um arquivo: {self.path}")
