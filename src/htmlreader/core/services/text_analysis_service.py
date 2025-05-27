"""
Serviço para análise de texto no HTMLReader.

Este módulo fornece funções para contar palavras e linhas em arquivos,
além de realizar contagem em lote em diretórios.
"""

from htmlreader.core.models.file_model import FileModel
from htmlreader.core.models.directory_model import DirectoryModel


class TextAnalysisService:
    """
    Serviço para análise de arquivos de texto.
    """

    @staticmethod
    def count_words(file: FileModel) -> int:
        """
        Conta o número de palavras no conteúdo do arquivo.

        Args:
            file (FileModel): Arquivo a ser analisado.

        Returns:
            int: Número de palavras.
        """
        return len(file.content.split()) if file.content else 0

    @staticmethod
    def count_lines(file: FileModel) -> int:
        """
        Conta o número de linhas no conteúdo do arquivo.

        Args:
            file (FileModel): Arquivo a ser analisado.

        Returns:
            int: Número de linhas.
        """
        return len(file.content.splitlines()) if file.content else 0

    @staticmethod
    def batch_count_words(directory: DirectoryModel) -> dict[str, int]:
        """
        Conta o número de palavras em cada arquivo do diretório.

        Args:
            directory (DirectoryModel): Diretório contendo os arquivos.

        Returns:
            dict[str, int]: Dicionário com o nome do arquivo e a contagem de palavras.
        """
        return {
            f.path.name: TextAnalysisService.count_words(f) for f in directory.files
        }
