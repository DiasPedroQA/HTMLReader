"""
Controlador de operações de criação e leitura de arquivos.

Utiliza a classe `Arquivo` para realizar operações como:
- Criação condicional de arquivos
- Escrita com controle de sobrescrita
- Leitura de conteúdo e metadados
"""

from pathlib import Path

from core.models.model_arquivo import Arquivo


class ArquivosController:
    """Controlador de operações de criação e leitura de arquivos."""

    def criar_arquivo(self, caminho_arquivo: str | Path, conteudo: str = "") -> Arquivo:
        """
        Cria um arquivo e escreve conteúdo, se fornecido.

        Args:
            caminho_arquivo (str | Path): Caminho do arquivo a ser criado.
            conteudo (str): Conteúdo opcional a ser escrito.

        Returns:
            Arquivo: Instância do arquivo criado ou existente.
        """
        objeto_arquivo = Arquivo(caminho=caminho_arquivo)
        if conteudo:
            objeto_arquivo.escrever_conteudo(conteudo_arquivo=conteudo, sobrescrever=False)
        else:
            objeto_arquivo.criar_arquivo_se_nao_existir()
        return objeto_arquivo

    def ler_conteudo_arquivo(self, caminho_arquivo: str | Path) -> str | None:
        """
        Lê o conteúdo de um arquivo.

        Args:
            caminho_arquivo (str | Path): Caminho do arquivo a ser lido.

        Returns:
            str | None: Conteúdo do arquivo.
        """
        objeto_arquivo = Arquivo(caminho=caminho_arquivo)
        return objeto_arquivo.ler_conteudo()

    def ler_metadados_arquivo(self, caminho_arquivo: str | Path) -> dict[str, str | None]:
        """
        Lê informações de metadados de um arquivo, sem o conteúdo.

        Args:
            caminho_arquivo (str | Path): Caminho do arquivo a ser lido.

        Returns:
            dict[str, str | None]: Dicionário com metadados sem o conteúdo do arquivo.
        """
        objeto_arquivo = Arquivo(caminho=caminho_arquivo)
        return {
            "nome": objeto_arquivo.nome_caminho,
            "nome_sem_extensao": objeto_arquivo.nome_sem_extensao,
            "extensao": objeto_arquivo.extensao,
            "extensao_legivel": objeto_arquivo.extensao_legivel,
            "tamanho_legivel": objeto_arquivo.tamanho_legivel,
            "eh_oculto": "Sim" if objeto_arquivo.eh_arquivo_oculto else "Não",
            "data_criacao": objeto_arquivo.data_criacao_legivel,
            "data_modificacao": objeto_arquivo.data_modificacao_legivel,
        }
