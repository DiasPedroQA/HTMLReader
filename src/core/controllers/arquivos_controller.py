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

    def criar_arquivo(self, caminho: str | Path, conteudo: str = "") -> Arquivo:
        """
        Cria um arquivo e escreve conteúdo, se fornecido.

        Args:
            caminho (str | Path): Caminho do arquivo a ser criado.
            conteudo (str): Conteúdo opcional a ser escrito.

        Returns:
            Arquivo: Instância do arquivo criado ou existente.
        """
        arquivo = Arquivo(caminho=caminho)
        if conteudo:
            arquivo.escrever_conteudo(conteudo_arquivo=conteudo, sobrescrever=False)
        else:
            arquivo.criar_se_nao_existir()
        return arquivo

    def ler_arquivo(self, caminho: str | Path) -> dict[str, str | None]:
        """
        Lê informações e conteúdo de um arquivo.

        Args:
            caminho (str | Path): Caminho do arquivo a ser lido.

        Returns:
            dict[str, str | None]: Dicionário com metadados e conteúdo do arquivo.
        """
        arquivo = Arquivo(caminho=caminho)
        return {
            "nome": arquivo.nome_caminho,
            "nome_sem_extensao": arquivo.nome_sem_extensao,
            "extensao": arquivo.extensao,
            "extensao_legivel": arquivo.extensao_legivel,
            "tamanho_legivel": arquivo.tamanho_legivel,
            "eh_oculto": "Sim" if arquivo.eh_arquivo_oculto else "Não",
            "data_modificacao": arquivo.data_modificacao_formatada,
            "conteudo": arquivo.ler_conteudo(),
        }
