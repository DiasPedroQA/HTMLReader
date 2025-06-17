"""
Módulo que define a classe ModelArquivo para
representar e manipular arquivos no sistema de arquivos.

Extende a funcionalidade de ModelCaminho com
características específicas de arquivos,
como extensão e conversão para dicionário.

Classes:
    ModelArquivo: Classe que representa um arquivo no sistema de arquivos, herdando de ModelCaminho.
"""

from pathlib import Path
from core.models.base_item import ModelCaminho


class ModelArquivo(ModelCaminho):
    """
    Representa um arquivo no sistema de arquivos.
    Herda de ModelCaminho e adiciona funcionalidades específicas para arquivos.

    Attributes:
        extensao (str): Extensão do arquivo em letras minúsculas.
    """

    def __init__(self, path: Path) -> None:
        """Inicializa o ModelArquivo verificando se o caminho é um arquivo válido.

        Args:
            path (Path): Caminho do arquivo no sistema de arquivos.

        Raises:
            ValueError: Se o caminho não corresponder a um arquivo existente.
        """
        super().__init__(caminho_bruto=path)

        if not self.caminho_bruto.is_file():
            raise ValueError(
                f"O caminho informado não é um arquivo: {self.caminho_bruto}"
            )

        self.extensao: str = self.caminho_bruto.suffix.lower()

    def para_dict(self) -> dict[str, str | int]:
        """Converte as propriedades do arquivo para um dicionário.

        Returns:
            dict: Dicionário contendo todas as propriedades relevantes do arquivo,
                  incluindo tipo, nome, extensão, caminho, tamanho e datas.
        """
        return {
            "tipo": "arquivo",
            "nome": self.nome,
            "extensao": self.extensao,
            "caminho": self.caminho,
            "tamanho": self.tamanho_bytes,
            "criado_em": self.data_criacao.isoformat(),
            "modificado_em": self.data_modificacao.isoformat(),
        }
