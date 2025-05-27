"""
Serviço para leitura e escrita de arquivos de texto no HTMLReader.

Este módulo fornece funções para ler e escrever arquivos de texto utilizando FileModel.
"""

from pathlib import Path
from htmlreader.core.models.file_model import FileModel
from htmlreader.core.utils.encoding_utils import detect_encoding
from htmlreader.core.utils.file_utils import read_binary


class TextFileService:
    """
    Serviço para operações de leitura e escrita de arquivos de texto.
    """

    @staticmethod
    def read(file: FileModel) -> FileModel:
        """
        Lê o conteúdo de um arquivo e atualiza o FileModel com o conteúdo e a codificação detectada.

        Args:
            file (FileModel): Instância de FileModel a ser lida.

        Returns:
            FileModel: O mesmo FileModel com os campos 'encoding' e 'content' preenchidos.
        """
        raw: bytes = read_binary(file.path)
        encoding: str = detect_encoding(file.path)
        file.encoding = encoding
        file.content = raw.decode(encoding)
        return file

    @staticmethod
    def write(file: FileModel, destination: Path) -> None:
        """
        Escreve o conteúdo do FileModel em um arquivo de destino.

        Args:
            file (FileModel): Instância de FileModel a ser escrita.
            destination (Path): Caminho do arquivo de destino.

        Returns:
            None: Não retorna nada.
        """
        destination.write_text(file.content or "", encoding=file.encoding)
