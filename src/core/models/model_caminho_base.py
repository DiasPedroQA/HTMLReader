"""
Módulo de abstrações para caminhos no sistema de arquivos.

Este módulo fornece uma estrutura orientada a objetos para representar caminhos
genéricos, arquivos e pastas, com capacidade de manipulação e verificação de existência.

Classes:
    TipoCaminho (Enum): Enumeração que representa o tipo de caminho.
    CaminhoBase (ABC): Classe abstrata base para qualquer tipo de caminho no sistema.
"""

from abc import ABC
from enum import Enum
from pathlib import Path
from os import stat_result
from datetime import datetime


class TipoCaminho(str, Enum):
    """
    Enumeração que define os tipos possíveis de caminhos no sistema de arquivos.

    Valores:
        ARQUIVO: Representa um arquivo comum.
        PASTA: Representa um diretório.
        DESCONHECIDO: Tipo indefinido ou inexistente.
    """

    ARQUIVO = "Arquivo"
    PASTA = "Pasta"
    DESCONHECIDO = "_*-*_"


class CaminhoBase(ABC):
    """
    Classe abstrata base para representação de caminhos no sistema de arquivos.

    Esta classe define a interface comum e propriedades compartilhadas por arquivos
    e diretórios, como verificação de existência, tipo de caminho, nome, data de
    modificação e tamanho em bytes.

    Atributos:
        _path (Path): Caminho absoluto do sistema de arquivos.
        _existe (bool): Indica se o caminho existe fisicamente.
        _tipo_caminho (TipoCaminho): Tipo do caminho identificado.
        _data_criacao (datetime | None): Data da criação.
        _data_modificacao (datetime | None): Data da última modificação.
        _tamanho_bytes (int | None): Tamanho do conteúdo em bytes.
    """

    def __init__(self, caminho: str | Path) -> None:
        """
        Inicializa a instância com base em uma string ou objeto Path.

        Args:
            caminho (str | Path): Caminho a ser representado.
        """
        self._path: Path = Path(caminho).expanduser().absolute()
        self._atualizar_estado()

    def _atualizar_estado(self) -> None:
        """
        Atualiza o estado interno do objeto.

        Define a existência do caminho, seu tipo (arquivo, pasta ou desconhecido),
        data da última modificação e tamanho em bytes.
        """
        self._existe: bool = self._path.exists()
        self._tipo_caminho: TipoCaminho = (
            TipoCaminho.ARQUIVO
            if self._path.is_file()
            else TipoCaminho.PASTA
            if self._path.is_dir()
            else TipoCaminho.DESCONHECIDO
        )

        if self._existe:
            try:
                stat: stat_result = self._path.stat()
                self._data_criacao: datetime | None = datetime.fromtimestamp(
                    timestamp=stat.st_mtime
                )
                self._data_modificacao: datetime | None = datetime.fromtimestamp(
                    timestamp=stat.st_ctime
                )
                self._tamanho_bytes: int | None = stat.st_size
            except OSError:
                self._data_criacao = None
                self._data_modificacao = None
                self._tamanho_bytes = None
        else:
            self._data_criacao = None
            self._data_modificacao = None
            self._tamanho_bytes = None

    @property
    def retornar_o_tipo(self) -> TipoCaminho:
        """
        Retorna o tipo de caminho identificado (arquivo, pasta ou desconhecido).

        Returns:
            TipoCaminho: Enumeração correspondente ao tipo do caminho.
        """
        return self._tipo_caminho

    @property
    def caminho_absoluto(self) -> Path:
        """
        Retorna o caminho absoluto como objeto `Path`.

        Returns:
            Path: Caminho completo no sistema de arquivos.
        """
        return self._path

    @property
    def caminho_existe(self) -> bool:
        """
        Verifica se o caminho existe fisicamente no sistema de arquivos.

        Returns:
            bool: True se o caminho existe, False caso contrário.
        """
        return self._existe

    @property
    def nome_caminho(self) -> str:
        """
        Retorna o nome final do caminho (arquivo ou pasta).

        Returns:
            str: Nome do arquivo ou diretório.
        """
        return self._path.name

    @property
    def data_criacao(self) -> datetime | None:
        """
        Retorna a data da criação, se disponível.

        Returns:
            datetime | None: Data de criação ou None se não aplicável.
        """
        return self._data_criacao

    @property
    def data_modificacao(self) -> datetime | None:
        """
        Retorna a data da última modificação, se disponível.

        Returns:
            datetime | None: Data de modificação ou None se não aplicável.
        """
        return self._data_modificacao

    @property
    def tamanho_em_bytes(self) -> int | None:
        """
        Retorna o tamanho do conteúdo em bytes, se aplicável.

        Returns:
            int | None: Tamanho em bytes, ou None se não aplicável.
        """
        return self._tamanho_bytes

    def __str__(self) -> str:
        """
        Retorna a representação textual do caminho (forma absoluta).

        Returns:
            str: Representação como string do caminho absoluto.
        """
        return str(self._path)
