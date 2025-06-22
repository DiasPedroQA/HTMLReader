"""
Módulo de abstrações para caminhos no sistema de arquivos.

Este módulo fornece uma estrutura orientada a objetos para representar caminhos
genéricos, arquivos e pastas, com capacidade de manipulação e verificação de existência.

Classes:
    TipoCaminho (Enum): Representa o tipo de caminho (arquivo, pasta, desconhecido).
    CaminhoBase (ABC): Classe abstrata base para caminhos, com atributos e comportamentos comuns.
"""

from abc import ABC
from datetime import datetime
from enum import Enum
from os import stat_result
from pathlib import Path


class TipoCaminho(str, Enum):
    """Enumeração que define os tipos possíveis de caminhos no sistema de arquivos."""

    ARQUIVO = "Arquivo"
    PASTA = "Pasta"
    DESCONHECIDO = "_*-*_"


class CaminhoBase(ABC):
    """
    Classe abstrata base para representação de caminhos no sistema de arquivos.

    Atributos:
        caminho_absoluto (Path): Caminho absoluto do sistema.
        caminho_existe (bool): Indica se o caminho caminho_existe fisicamente.
        retornar_o_tipo (TipoCaminho): Tipo do caminho (arquivo, pasta, desconhecido).
        data_criacao (datetime | None): Data de criação.
        data_modificacao (datetime | None): Data da última modificação.
        tamanho_bytes (int | None): Tamanho em bytes do conteúdo.
    """

    def __init__(self, caminho: str | Path) -> None:
        """
        Inicializa a instância com base em um caminho absoluto.

        Args:
            caminho (str | Path): Caminho a ser representado.
        """
        self._path: Path = Path(caminho).expanduser().absolute()
        self._atualizar_estado()

    def _atualizar_estado(self) -> None:
        """Atualiza os dados internos do caminho (existência, tipo, datas, tamanho)."""
        self._existe: bool = self._path.exists()

        if self._path.is_file():
            self._tipo: TipoCaminho = TipoCaminho.ARQUIVO
        elif self._path.is_dir():
            self._tipo: TipoCaminho = TipoCaminho.PASTA
        else:
            self._tipo: TipoCaminho = TipoCaminho.DESCONHECIDO

        try:
            stat: stat_result = self._path.stat()
            self._data_criacao: datetime | None = datetime.fromtimestamp(timestamp=stat.st_ctime)
            self._data_modificacao: datetime | None = datetime.fromtimestamp(timestamp=stat.st_mtime)
            self._tamanho_bytes: int | None = stat.st_size
        except OSError:
            self._data_criacao = None
            self._data_modificacao = None
            self._tamanho_bytes = None

    @property
    def retornar_o_tipo(self) -> TipoCaminho:
        """Retorna o tipo do caminho (arquivo, pasta, desconhecido)."""
        return self._tipo

    @property
    def caminho_absoluto(self) -> Path:
        """Retorna o caminho absoluto."""
        return self._path

    @property
    def caminho_existe(self) -> bool:
        """Indica se o caminho existe fisicamente no sistema."""
        return self._existe

    @property
    def nome_caminho(self) -> str:
        """Retorna o nome do arquivo ou pasta (último componente do caminho)."""
        return self._path.name

    @property
    def data_criacao(self) -> datetime | None:
        """Data da criação, se disponível."""
        return self._data_criacao

    @property
    def data_modificacao(self) -> datetime | None:
        """Data da última modificação, se disponível."""
        return self._data_modificacao

    @property
    def tamanho_bytes(self) -> int | None:
        """Tamanho do conteúdo em bytes, se aplicável."""
        return self._tamanho_bytes

    def __str__(self) -> str:
        """Representação textual do caminho absoluto."""
        return str(self._path)
