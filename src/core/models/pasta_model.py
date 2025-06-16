"""
Utilitários para obtenção de informações do sistema operacional,
usando um modelo de objetos com herança para representar a hierarquia
de arquivos e diretórios.
"""

# import json
import json
from os import stat_result
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from typing import TypedDict

from core.utils.formatadores import (
    converter_bytes_em_tamanho_legivel,
    formatar_data_para_string,
)


class PastaFormatadaDict(TypedDict):
    """Dicionário tipado que representa uma pasta formatada para saída.

    Atributos:
        nome_da_pasta (str): Nome da pasta
        caminho_absoluto (str): Caminho completo da pasta
        tamanho_total (str): Tamanho total formatado (ex: "1.2 MB")
        criada_em (str): Data de criação formatada
        modificada_em (str): Data de modificação formatada
        subarquivos (list[str]): Lista de nomes de arquivos contidos
        subpastas (list[PastaFormatadaDict]): Lista de subpastas formatadas
    """

    nome_da_pasta: str
    caminho_absoluto: str
    tamanho_total: str
    criada_em: str
    modificada_em: str
    subarquivos: list[str]
    subpastas: list["PastaFormatadaDict"]


@dataclass(frozen=True, slots=True)
class ItemDoSistema(ABC):
    """Classe base abstrata que representa uma entidade no sistema de arquivos.

    Esta classe não pode ser instanciada diretamente. Ela define os atributos
    e comportamentos comuns a arquivos e pastas.

    Atributos:
        nome (str): Nome do item
        caminho_absoluto (str): Caminho completo para o item
        tamanho_em_bytes (int): Tamanho do item em bytes
        data_de_criacao (datetime): Data de criação do item
        data_da_ultima_modificacao (datetime): Data da última modificação
    """

    nome: str
    caminho_absoluto: str
    tamanho_em_bytes: int
    data_de_criacao: datetime
    data_da_ultima_modificacao: datetime

    @abstractmethod
    def para_dict_formatado(
        self, recursivo: bool = False
    ) -> dict[str, str] | PastaFormatadaDict:
        """Converte o item para um dicionário formatado."""

    @staticmethod
    def from_caminho(caminho_fornecido: str | Path) -> "ItemDoSistema":
        """Método fábrica que cria um objeto Pasta ou Arquivo conforme o caminho.

        Args:
            caminho_fornecido (str | Path): Caminho do arquivo ou diretório

        Returns:
            ItemDoSistema: Instância de Pasta ou Arquivo

        Raises:
            FileNotFoundError: Se o caminho não existir
            ValueError: Se o caminho não for um arquivo ou diretório válido
        """
        path: Path = Path(caminho_fornecido).resolve()

        if not path.exists():
            raise FileNotFoundError(f"O caminho não foi encontrado: {path}")

        if path.is_dir():
            return Pasta.construir_pasta_recursivamente(path)
        if path.is_file():
            return Arquivo.construir_arquivo(path)

        raise ValueError(f"O caminho não é um arquivo nem um diretório válido: {path}")


@dataclass(frozen=True, slots=True)
class Arquivo(ItemDoSistema):
    """Representa um arquivo no sistema de arquivos.

    Herda de ItemDoSistema e implementa os métodos abstratos.
    """

    @classmethod
    def construir_arquivo(cls, path: Path) -> "Arquivo":
        """Constrói uma instância de Arquivo a partir de um caminho.

        Args:
            path (Path): Caminho para o arquivo

        Returns:
            Arquivo: Nova instância de Arquivo com os metadados do arquivo
        """
        stats: stat_result = path.stat()
        return cls(
            nome=path.name,
            caminho_absoluto=str(path),
            tamanho_em_bytes=stats.st_size,
            data_de_criacao=datetime.fromtimestamp(stats.st_ctime),
            data_da_ultima_modificacao=datetime.fromtimestamp(stats.st_mtime),
        )

    def para_dict_formatado(self, recursivo: bool = False) -> dict[str, str]:
        """Retorna uma representação em dicionário formatado do arquivo.

        Args:
            recursivo (bool, optional): Ignorado para arquivos. Mantido para compatibilidade.
                                      Padrão: False.

        Returns:
            dict[str, str]: Dicionário com nome, tamanho e data de criação formatados
        """
        return {
            "tipo": "Arquivo",
            "nome": self.nome,
            "tamanho": converter_bytes_em_tamanho_legivel(
                tamanho_bytes=self.tamanho_em_bytes
            ),
            "criado_em": formatar_data_para_string(data_e_hora=self.data_de_criacao),
        }


@dataclass(frozen=True, slots=True)
class Pasta(ItemDoSistema):
    """Representa uma pasta/diretório no sistema de arquivos.

    Herda de ItemDoSistema e adiciona capacidade de conter outros itens.

    Atributos:
        subpastas (list[Pasta]): Lista de subpastas contidas
        subarquivos (list[Arquivo]): Lista de arquivos contidos
    """

    subpastas: list["Pasta"] = field(default_factory=list)
    subarquivos: list[Arquivo] = field(default_factory=list)

    @classmethod
    def construir_pasta_recursivamente(cls, path: Path) -> "Pasta":
        """Constrói uma pasta e seu conteúdo de forma recursiva.

        Args:
            path (Path): Caminho para a pasta raiz

        Returns:
            Pasta: Nova instância de Pasta com todo o conteúdo recursivamente
        """
        lista_subpastas: list["Pasta"] = []
        lista_subarquivos: list[Arquivo] = []

        for item_path in path.iterdir():
            sub_item: ItemDoSistema = ItemDoSistema.from_caminho(
                caminho_fornecido=str(item_path)
            )
            if isinstance(sub_item, Pasta):
                lista_subpastas.append(sub_item)
            elif isinstance(sub_item, Arquivo):
                lista_subarquivos.append(sub_item)

        tamanho_total: int = sum(a.tamanho_em_bytes for a in lista_subarquivos) + sum(
            p.tamanho_em_bytes for p in lista_subpastas
        )

        stats_pasta: stat_result = path.stat()
        return cls(
            nome=path.name,
            caminho_absoluto=str(path),
            tamanho_em_bytes=tamanho_total,
            data_de_criacao=datetime.fromtimestamp(stats_pasta.st_ctime),
            data_da_ultima_modificacao=datetime.fromtimestamp(stats_pasta.st_mtime),
            subpastas=lista_subpastas,
            subarquivos=lista_subarquivos,
        )

    def para_dict_formatado(self, recursivo: bool = False) -> PastaFormatadaDict:
        # Implementação específica para pastas
        dados: PastaFormatadaDict = {
            "nome_da_pasta": self.nome,
            "caminho_absoluto": self.caminho_absoluto,
            "tamanho_total": converter_bytes_em_tamanho_legivel(
                tamanho_bytes=self.tamanho_em_bytes
            ),
            "criada_em": formatar_data_para_string(data_e_hora=self.data_de_criacao),
            "modificada_em": formatar_data_para_string(
                data_e_hora=self.data_da_ultima_modificacao
            ),
            "subarquivos": [arquivo.nome for arquivo in self.subarquivos],
            "subpastas": [
                subpasta.para_dict_formatado(recursivo=False)
                for subpasta in self.subpastas
            ],
        }

        if recursivo:
            dados["subpastas"] = [
                subpasta.para_dict_formatado(recursivo=True)
                for subpasta in self.subpastas
            ]
        return dados


# Exemplo de uso do novo modelo

try:
    # O método fábrica decide se cria uma Pasta ou um Arquivo
    item_raiz: ItemDoSistema = ItemDoSistema.from_caminho(
        caminho_fornecido="/home/pedro-pm-dias/Downloads/Firefox"
    )

    # Agora, verificamos o tipo do item retornado
    if isinstance(item_raiz, Pasta):
        print(f"O item é uma PASTA: {item_raiz.nome}")
        print(
            f"Ela contém {len(item_raiz.subarquivos)} arquivo(s) e"
            f" {len(item_raiz.subpastas)} subpasta(s)."
        )

        # Exibindo o conteúdo da pasta
        for arquivo in item_raiz.subarquivos:
            print(f"  - Arquivo: {arquivo.nome}")

        for subpasta in item_raiz.subpastas:
            print(f"  - Subpasta: {subpasta.nome} (Tamanho: {converter_bytes_em_tamanho_legivel(tamanho_bytes=subpasta.tamanho_em_bytes)})")

        # Usando o método para_dict_formatado que existe na Pasta
        print("\n--- Dicionário Formatado da Pasta ---")
        print(
            json.dumps(
                item_raiz.para_dict_formatado(recursivo=False),
                indent=4,
                ensure_ascii=False,
            )
        )

    # Corrigindo a parte do código com o erro (linha 294 aproximadamente)
    elif isinstance(item_raiz, Arquivo):
        print(f"O item é um ARQUIVO: {item_raiz.nome}")
        tamanho_formatado = converter_bytes_em_tamanho_legivel(
            tamanho_bytes=item_raiz.tamanho_em_bytes
        )
        print(f"Tamanho: {tamanho_formatado}")

        # Usando o método para_dict_formatado que existe no Arquivo
        print("\n--- Dicionário Formatado do Arquivo ---")
        print(json.dumps(item_raiz.para_dict_formatado(), indent=4, ensure_ascii=False))

except (ValueError, FileNotFoundError) as e:
    print(f"Ocorreu um erro: {e}")
