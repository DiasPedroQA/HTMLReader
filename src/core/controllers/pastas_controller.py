"""
Controlador de operações com diretórios no sistema de arquivos.

A classe `PastasController` fornece métodos para criação segura de pastas,
leitura de conteúdo imediato ou recursivo e identificação de arquivos/pastas ocultos.
"""

from pathlib import Path

from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta


class PastasController:
    """
    Controlador para leitura e criação de diretórios usando a model Pasta.
    """

    def listar_nomes_itens(self, caminho: str | Path) -> list[str]:
        """
        Retorna os nomes de todos os itens diretamente contidos na pasta.

        Args:
            caminho: Caminho da pasta a ser lida.

        Returns:
            Lista com os nomes dos arquivos e subpastas.
        """
        pasta = Pasta(caminho=caminho)
        return [item.nome_caminho for item in pasta.itens_diretos]

    def listar_ocultos(self, caminho: str | Path) -> list[Path]:
        """
        Retorna os caminhos de itens ocultos diretamente contidos na pasta.

        Args:
            caminho: Caminho da pasta a ser inspecionada.

        Returns:
            Lista de caminhos de arquivos ou pastas ocultos.
        """
        pasta = Pasta(caminho=caminho)
        return pasta.listar_ocultos()

    def listar_conteudo_recursivo(self, caminho: str | Path) -> list[CaminhoBase]:
        """
        Retorna todos os arquivos e subpastas contidos, de forma recursiva.

        Args:
            caminho: Caminho base da leitura.

        Returns:
            Lista de objetos CaminhoBase representando cada item encontrado.
        """
        pasta = Pasta(caminho=caminho)
        return pasta.listar_conteudo_recursivo() if pasta.caminho_existe else []

    def criar_se_nao_existir(self, caminho: Path) -> bool:
        """
        Cria o diretório no caminho informado, caso ainda não exista.

        Args:
            caminho: Caminho da nova pasta.

        Returns:
            True se a pasta foi criada, False se já existia.
        """
        pasta = Pasta(caminho=caminho)
        if not pasta.caminho_existe:
            pasta.caminho_absoluto.mkdir(parents=True, exist_ok=True)
            return True
        return False

    def listar_subpastas(self, caminho: Path) -> list[Pasta]:
        """
        Retorna as subpastas diretamente contidas na pasta informada.

        Args:
            caminho: Caminho da pasta principal.

        Returns:
            Lista de objetos Pasta representando as subpastas imediatas.
        """
        pasta = Pasta(caminho=caminho)
        return [Pasta(caminho=item.caminho_absoluto) for item in pasta.itens_diretos if item.retornar_o_tipo == "Pasta"]

    def listar_arquivos(self, caminho: Path, extensao: str | None = None) -> list[Arquivo]:
        """
        Retorna os arquivos diretamente contidos, com opção de filtrar por extensão.

        Args:
            caminho: Caminho da pasta a ser inspecionada.
            extensao: Extensão dos arquivos desejados (ex: '.txt').

        Returns:
            Lista de objetos Arquivo encontrados.
        """
        pasta_atual = Pasta(caminho=caminho)
        lista_arquivos_pasta_atual: list[Arquivo] = [
            Arquivo(caminho=item.caminho_absoluto)
            for item in pasta_atual.itens_diretos
            if item.retornar_o_tipo == "Arquivo"
        ]
        if len(lista_arquivos_pasta_atual) == 0:
            print(f"Nenhum arquivo encontrado na pasta {pasta_atual.caminho_absoluto}")
        if extensao:
            return [arquivo for arquivo in lista_arquivos_pasta_atual if arquivo.extensao_legivel == extensao]
        return lista_arquivos_pasta_atual
