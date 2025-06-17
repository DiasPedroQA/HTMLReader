"""
Módulo que define a classe ModelPasta para representar
e manipular diretórios no sistema de arquivos.

Extende a funcionalidade de ModelCaminho com características específicas de pastas/diretórios,
incluindo a capacidade de listar seus conteúdos de forma seletiva e recursiva.

Classes:
    ModelPasta: Classe que representa um diretório no sistema de arquivos, herdando de ModelCaminho.
"""

from pathlib import Path

from core.models.base_item import ModelCaminho
from core.models.arquivo_model import ModelArquivo


class ModelPasta(ModelCaminho):
    """
    Representa uma pasta/diretório no sistema de arquivos.
    Herda de ModelCaminho e adiciona funcionalidades específicas para diretórios.

    Attributes:
        caminho_bruto (Path): Herdado de ModelCaminho, contém o Path do diretório.
    """

    def __init__(self, path: Path) -> None:
        """Inicializa o ModelPasta verificando se o caminho é um diretório válido.

        Args:
            path (Path): Caminho do diretório no sistema de arquivos.

        Raises:
            ValueError: Se o caminho não corresponder a um diretório existente.
        """
        self.qtd_pastas: int = 0
        self.qtd_arquivos: int = 0
        super().__init__(caminho_bruto=path)

        if not self.caminho_bruto.is_dir():
            raise ValueError(
                f"O caminho informado não é uma pasta: {self.caminho_bruto}"
            )

    def listar_subitens(self, recursivo: bool = False) -> list[ModelCaminho]:
        """Lista todos os itens contidos na pasta (arquivos e subpastas).

        Args:
            recursivo (bool): Se True, lista itens de subpastas recursivamente.

        Returns:
            list[ModelCaminho]: Lista contendo ModelArquivo e ModelPasta dos itens encontrados.
        """
        subitens: list[ModelCaminho] = []

        for item in self.caminho_bruto.iterdir():
            try:
                if item.is_dir():
                    pasta = ModelPasta(item)
                    subitens.append(pasta)
                    if recursivo:
                        subitens.extend(pasta.listar_subitens(recursivo=True))
                elif item.is_file():
                    subitens.append(ModelArquivo(item))
            except OSError:
                continue

        return subitens

    def listar_arquivos(self, recursivo: bool = False) -> list[ModelArquivo]:
        """Lista apenas os arquivos contidos na pasta.

        Args:
            recursivo (bool): Se True, lista arquivos de subpastas recursivamente.

        Returns:
            list[ModelArquivo]: Lista de ModelArquivo contendo apenas arquivos.
        """
        return [
            item
            for item in self.listar_subitens(recursivo=recursivo)
            if isinstance(item, ModelArquivo)
        ]

    def listar_subpastas(self, recursivo: bool = False) -> list["ModelPasta"]:
        """Lista apenas as subpastas contidas na pasta.

        Args:
            recursivo (bool): Se True, lista subpastas recursivamente.

        Returns:
            list[ModelPasta]: Lista de ModelPasta contendo apenas diretórios.
        """
        return [
            item
            for item in self.listar_subitens(recursivo)
            if isinstance(item, ModelPasta)
        ]

    def contar_itens(self) -> tuple[int, int]:
        """Conta a quantidade de arquivos e subpastas contidos na pasta.

        Returns:
            Tuple[int, int]: (quantidade_arquivos, quantidade_pastas)
        """
        sub_arquivos: int = 0
        sub_pastas: int = 0

        for item in self.caminho_bruto.iterdir():
            try:
                if item.is_dir():
                    sub_pastas += 1
                elif item.is_file():
                    sub_arquivos += 1
            except OSError:
                continue

        return (sub_arquivos, sub_pastas)

    def para_dict(self) -> dict[str, str | int | list]:
        """Converte as propriedades da pasta para um dicionário.

        Returns:
            dict: Dicionário contendo propriedades da pasta,
                  incluindo tipo, nome, caminho, datas e contagem de itens.
        """
        self.qtd_arquivos, self.qtd_pastas = self.contar_itens()
        return {
            "tipo": "pasta",
            "nome": self.nome,
            "caminho": self.caminho,
            "criado_em": self.data_criacao.isoformat(),
            "modificado_em": self.data_modificacao.isoformat(),
            "quantidade_arquivos": self.qtd_arquivos,
            "quantidade_pastas": self.qtd_pastas,
            "tamanho_total": sum(f.tamanho_bytes for f in self.listar_arquivos()),
        }
