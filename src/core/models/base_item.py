"""
Módulo que define a classe ModelCaminho para
representar e manipular caminhos do sistema de arquivos.

Fornece uma interface orientada a objetos para trabalhar com arquivos e diretórios,
incluindo propriedades como nome, caminho absoluto, datas de criação/modificação,
tamanho e verificação de tipo (arquivo/diretório).

Classes:
    ModelCaminho: Classe principal que encapsula um caminho do sistema de arquivos.
"""

from pathlib import Path
from datetime import datetime


class ModelCaminho:
    """
    Representa um caminho genérico do sistema de arquivos.
    Pode ser um arquivo ou uma pasta.

    Attributes:
        caminho_bruto (Path): O objeto Path que representa o caminho no sistema de arquivos.
    """

    def __init__(self, caminho_bruto: Path) -> None:
        """Inicializa o ModelCaminho com um objeto Path.

        Args:
            caminho_bruto (Path): O caminho do arquivo ou pasta.

        Raises:
            TypeError: Se o caminho_bruto não for uma instância de Path.
        """
        if not isinstance(caminho_bruto, Path):
            raise TypeError(
                "O parâmetro 'caminho_bruto' deve ser uma instância de pathlib.Path."
            )
        self.caminho_bruto: Path = caminho_bruto.resolve()

    @property
    def nome(self) -> str:
        """Retorna o nome do arquivo ou pasta (incluindo extensão, se aplicável).

        Returns:
            str: O nome do arquivo ou pasta.
        """
        return self.caminho_bruto.name

    @property
    def caminho(self) -> str:
        """Retorna o caminho completo como string.

        Returns:
            str: O caminho absoluto como string.
        """
        return str(self.caminho_bruto)

    @property
    def data_criacao(self) -> datetime:
        """Retorna a data de criação do arquivo ou pasta.

        Returns:
            datetime: Objeto datetime representando a data de criação.
        """
        return datetime.fromtimestamp(self.caminho_bruto.stat().st_ctime)

    @property
    def data_modificacao(self) -> datetime:
        """Retorna a data de modificação do arquivo ou pasta.

        Returns:
            datetime: Objeto datetime representando a data de modificação.
        """
        return datetime.fromtimestamp(self.caminho_bruto.stat().st_mtime)

    @property
    def tamanho_bytes(self) -> int:
        """Retorna o tamanho em bytes (se for arquivo) ou 0 (se for pasta).

        Returns:
            int: Tamanho em bytes para arquivos, 0 para pastas.
        """
        return self.caminho_bruto.stat().st_size if self.caminho_bruto.is_file() else 0

    @property
    def eh_arquivo(self) -> bool:
        """Verifica se o caminho representa um arquivo.

        Returns:
            bool: True se for arquivo, False caso contrário.
        """
        return self.caminho_bruto.is_file()

    @property
    def eh_pasta(self) -> bool:
        """Verifica se o caminho representa uma pasta.

        Returns:
            bool: True se for pasta, False caso contrário.
        """
        return self.caminho_bruto.is_dir()

    def __repr__(self) -> str:
        """Representação string do objeto para debug.

        Returns:
            str: String no formato <Tipo: Nome>.
        """
        tipo: str = (
            "Arquivo"
            if self.eh_arquivo
            else "Pasta"
            if self.eh_pasta
            else "Desconhecido"
        )
        return f"<{tipo}: {self.nome}>"
