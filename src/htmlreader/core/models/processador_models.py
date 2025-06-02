"""
Modelos Pydantic para processamento de arquivos no HTMLReader.

Define schemas para validação de caminhos de arquivos, resultados de processamento
e lotes de arquivos.
"""

from pathlib import Path
from typing import List
from pydantic import BaseModel, validator


class CaminhoArquivo(BaseModel):
    """
    Modelo que representa um caminho de arquivo existente.

    Attributes:
        path (Path): Caminho para o arquivo.
    """

    path: Path

    @validator("path")
    def deve_existir_e_ser_arquivo(self, v: Path):
        """
        Valida se o caminho existe e é um arquivo.

        Args:
            v (Path): Caminho a ser validado.

        Raises:
            ValueError: Se o caminho não existir ou não for um arquivo.

        Returns:
            Path: O próprio caminho, se válido.
        """
        if not v.exists():
            raise ValueError("Arquivo não existe.")
        if not v.is_file():
            raise ValueError("O caminho deve ser um arquivo.")
        return v


class ResultadoProcessamento(BaseModel):
    """
    Modelo que representa o resultado do processamento de um arquivo.

    Attributes:
        entrada (Path): Caminho do arquivo de entrada.
        saida (Path): Caminho do arquivo de saída.
        sucesso (bool): Indica se o processamento foi bem-sucedido.
        mensagem (str): Mensagem adicional sobre o processamento.
    """

    entrada: Path
    saida: Path
    sucesso: bool
    mensagem: str


class LoteDeArquivos(BaseModel):
    """
    Modelo que representa um lote de arquivos para processamento.

    Attributes:
        arquivos (List[CaminhoArquivo]): Lista de caminhos de arquivos.
    """

    arquivos: List[CaminhoArquivo]
