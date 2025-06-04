# pylint: disable=no-self-argument

"""
Modelos Pydantic para o visor de arquivos e pastas do HTMLReader.

Define schemas para validação de caminhos, filtros, itens de pasta,
listas de itens e prévias de arquivos.
"""

from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class CaminhoEntrada(BaseModel):
    """
    Modelo que representa um caminho de entrada para arquivos ou pastas.

    Attributes:
        path (Path): Caminho do arquivo ou pasta.
    """

    path: Path

    @field_validator("path")
    @classmethod
    def path_deve_existir(cls, v: Path) -> Path:
        """
        Valida se o caminho existe.

        Args:
            v (Path): Caminho a ser validado.

        Raises:
            ValueError: Se o caminho não existir.

        Returns:
            Path: O próprio caminho, se válido.
        """
        if not v.exists():
            raise ValueError(f"O caminho '{v}' não existe.")
        return v


class FiltroVisor(BaseModel):
    """
    Modelo para filtro de arquivos e pastas no visor.

    Attributes:
        extensoes (list[str] | None): Lista de extensões para filtrar arquivos.
        tipo (str | None): Tipo de item a filtrar. Pode ser qualquer string ou None.
    """

    extensoes: list[str] | None = Field(default=None, description="Ex: ['.html']")
    tipo: str | None = None


class ItemDePasta(BaseModel):
    """
    Modelo que representa um item (arquivo ou pasta) dentro de um diretório.

    Attributes:
        nome (str): Nome do item.
        path (Path): Caminho do item.
        tipo (Literal['arquivo', 'pasta']): Tipo do item.
    """

    nome: str
    path: Path
    tipo: Literal["arquivo", "pasta"]


class ListaDeItens(BaseModel):
    """
    Modelo que representa uma lista de itens de pasta.

    Attributes:
        itens (list[ItemDePasta]): Lista de itens encontrados.
    """

    itens: list[ItemDePasta]

    def __len__(self) -> int:
        """
        Retorna a quantidade de itens na lista.
        """
        return len(self.itens)


class PreviaArquivo(BaseModel):
    """
    Modelo que representa uma prévia de um arquivo.

    Attributes:
        nome (str): Nome do arquivo.
        extensao (str): Extensão do arquivo.
        tamanho_bytes (int): Tamanho do arquivo em bytes.
        modificado_em (str): Data/hora da última modificação.
        linhas (list[str]): Linhas do conteúdo do arquivo.
    """

    nome: str
    extensao: str
    tamanho_bytes: int
    modificado_em: str
    linhas: list[str]
