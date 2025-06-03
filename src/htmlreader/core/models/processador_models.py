"""
Modelos Pydantic para processamento de arquivos no HTMLReader.

Define schemas para validação de caminhos de arquivos, resultados de processamento
e lotes de arquivos.
"""

from pathlib import Path
from pydantic import BaseModel, validator


class CaminhoArquivo(BaseModel):
    """
    Modelo que representa um caminho de arquivo existente.

    Attributes:
        path (Path): Caminho para o arquivo.
    """

    path: Path

    @validator("path")
    def deve_existir_e_ser_arquivo(cls, v: Path) -> Path:
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

    def __str__(self) -> str:
        """
        Retorna uma representação legível do resultado do processamento.
        """
        status = "Sucesso" if self.sucesso else "Falha"
        return f"{status}: {self.entrada} → {self.saida} | {self.mensagem}"


class LoteDeArquivos(BaseModel):
    """
    Modelo que representa um lote de arquivos para processamento.

    Attributes:
        arquivos (list[CaminhoArquivo]): Lista de caminhos de arquivos.
    """

    arquivos: list[CaminhoArquivo]

    def __len__(self) -> int:
        """
        Retorna a quantidade de arquivos no lote.
        """
        return len(self.arquivos)


# Exceções customizadas
class CaminhoInvalidoError(Exception):
    """
    Exceção para indicar que um caminho fornecido é inválido.
    """

    def __init__(self, mensagem: str = "Caminho inválido."):
        super().__init__(mensagem)


class ArquivoNaoSuportadoError(Exception):
    """
    Exceção para indicar que o arquivo fornecido não é suportado pelo sistema.
    """

    def __init__(self, mensagem: str = "Arquivo não suportado."):
        super().__init__(mensagem)


class ErroDeProcessamento(Exception):
    """
    Exceção para indicar erro durante o processamento de arquivos.
    """

    def __init__(self, mensagem: str = "Erro durante o processamento do arquivo."):
        super().__init__(mensagem)
