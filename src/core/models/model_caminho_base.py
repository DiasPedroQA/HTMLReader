"""
Módulo de abstrações para caminhos no sistema de arquivos.

Define uma estrutura orientada a objetos para representar caminhos genéricos,
arquivos e pastas, com capacidade de manipulação e verificação de existência.

Classes:
    - CaminhoBase: Classe abstrata que define a interface comum para qualquer tipo de caminho.
    - Arquivo: Representa um arquivo. Permite criação e leitura condicional do conteúdo.
    - Pasta: Representa uma pasta. Permite criação e listagem de conteúdo recursivo.
"""

from pathlib import Path
from abc import ABC, abstractmethod


class CaminhoBase(ABC):
    """Classe base abstrata para representar um caminho do sistema de arquivos."""

    def __init__(self, caminho: str | Path) -> None:
        self._path: Path = Path(caminho).expanduser().absolute()
        self._atualizar_estado()

    def _atualizar_estado(self) -> None:
        """Atualiza o estado interno de existência."""
        self._existe: bool = self._path.exists()

    @property
    def caminho_absoluto(self) -> Path:
        """Retorna o caminho absoluto como objeto Path."""
        return self._path

    @property
    def caminho_existe(self) -> bool:
        """Indica se o caminho existe fisicamente no sistema."""
        return self._existe

    @property
    def nome_caminho(self) -> str:
        """Retorna apenas o nome do último componente do caminho."""
        return self._path.name

    def __str__(self) -> str:
        return str(self._path)

    @abstractmethod
    def criar_se_nao_existir(self) -> bool:
        """Cria o caminho no sistema de arquivos, se não existir."""
        ...  # pylint: disable=unnecessary-ellipsis


class Arquivo(CaminhoBase):
    """Representa um arquivo no sistema de arquivos."""

    def criar_se_nao_existir(self) -> bool:
        """Cria o arquivo apenas se ele ainda não existir."""
        if self.caminho_existe:
            return False
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch()
            self._atualizar_estado()
            return True
        except OSError as erro:
            print(f"Erro ao criar arquivo: {erro}")
            return False

    def escrever_conteudo(self, conteudo: str) -> bool:
        """Escreve conteúdo no arquivo somente se ele ainda não existir.

        Retorna:
            bool: True se o arquivo foi criado e escrito com sucesso.
        """
        if self.caminho_existe:
            print("Arquivo já existe. Escrita não permitida.")
            return False

        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(file=self._path, mode="x", encoding="utf-8") as arquivo_destino:
                arquivo_destino.write(conteudo)
            self._atualizar_estado()
            return True
        except OSError as erro:
            print(f"Erro ao escrever no arquivo: {erro}")
            return False

    def ler_conteudo(self) -> str | None:
        """Lê e retorna o conteúdo do arquivo, se existir."""
        if not self.caminho_existe:
            return None
        try:
            return self._path.read_text(encoding="utf-8")
        except OSError as erro:
            print(f"Erro ao ler o arquivo: {erro}")
            return None


class Pasta(CaminhoBase):
    """Representa uma pasta no sistema de arquivos."""

    def criar_se_nao_existir(self) -> bool:
        """Cria a pasta apenas se ela ainda não existir."""
        if self.caminho_existe:
            return False
        try:
            self._path.mkdir(parents=True)
            self._atualizar_estado()
            return True
        except OSError as erro:
            print(f"Erro ao criar pasta: {erro}")
            return False

    def listar_conteudo(self) -> list[CaminhoBase]:
        """Lista os arquivos e subpastas da pasta atual.

        Retorna:
            list[CaminhoBase]: Objetos Arquivo ou Pasta para cada item.
        """
        if not self.caminho_existe:
            return []

        conteudo: list[CaminhoBase] = []
        for item in self._path.iterdir():
            if item.is_dir():
                conteudo.append(Pasta(caminho=item))
            elif item.is_file():
                conteudo.append(Arquivo(caminho=item))
        return conteudo
