"""
Módulo de controle para operações com diretórios no sistema de arquivos.

Este módulo define a classe `PastasController`, responsável por mediar a criação
e leitura de pastas, utilizando a model `Pasta` como base para operações de leitura
e escrita seguras.

Funcionalidades disponíveis:
- Criação condicional de diretórios
- Listagem de conteúdo imediato
- Identificação de arquivos e pastas ocultos
- Listagem recursiva completa
"""

from pathlib import Path

from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta


class PastasController:
    """
    Controlador de operações de criação e leitura de pastas no sistema de arquivos.

    Utiliza a model `Pasta` para aplicar regras e filtros.
    """

    def ler_nomes_dos_itens_da_pasta(self, caminho: str | Path) -> list[str]:
        """
        Retorna os nomes dos arquivos e subpastas contidos diretamente na pasta.

        Args:
            caminho: Caminho da pasta a ser lida.

        Returns:
            Lista de nomes de arquivos e subpastas.
        """
        objeto_pasta = Pasta(caminho=caminho)
        return [p.nome_caminho for p in objeto_pasta.conteudo_listado]

    def coletar_itens_ocultos(self, caminho: str | Path) -> list[Path]:
        """
        Retorna os caminhos de arquivos e pastas ocultos (iniciados com ponto).

        Args:
            caminho: Caminho da pasta a ser inspecionada.

        Returns:
            Lista de caminhos de itens ocultos.
        """
        objeto_pasta = Pasta(caminho=caminho)
        return objeto_pasta.coletar_itens_ocultos()

    def ler_recursivamente_caminhos_da_pasta(
        self, caminho: str | Path
    ) -> list[CaminhoBase]:
        """
        Lê recursivamente todos os arquivos e subpastas dentro da pasta informada.

        Args:
            caminho: Caminho base da varredura.

        Returns:
            Lista de objetos representando caminhos internos.
        """
        objeto_pasta = Pasta(caminho=caminho)
        return (
            objeto_pasta.coletar_itens_recursivamente()
            if objeto_pasta.caminho_existe
            else []
        )

    def criar_pasta_se_nao_existir(self, caminho_novo: Path) -> bool:
        """
        Cria a pasta no caminho indicado, se ela ainda não existir.

        Args:
            caminho_novo: Caminho do novo diretório.

        Returns:
            True se a pasta foi criada, False se já existia.
        """
        objeto_pasta = Pasta(caminho=caminho_novo)
        if not objeto_pasta.caminho_existe:
            objeto_pasta.caminho_absoluto.mkdir(parents=True, exist_ok=True)
            return True
        return False

    def ler_sub_pastas_de_uma_pasta(self, caminho_da_pasta: Path) -> list[Pasta]:
        """
        Retorna todas as subpastas imediatas de uma pasta fornecida.

        Args:
            caminho_da_pasta: Caminho da pasta a ser inspecionada.

        Returns:
            Lista de objetos `Pasta` representando subpastas.
        """
        objeto_pasta = Pasta(caminho=caminho_da_pasta)
        return [
            Pasta(caminho=pasta.caminho_absoluto)
            for pasta in objeto_pasta.conteudo_listado
            if pasta.retornar_o_tipo.value == "Pasta"
        ]

    def ler_sub_arquivos_de_uma_pasta(
        self, caminho_da_pasta: Path, extensao_buscada: str | None = None
    ) -> list[Arquivo]:
        """
        Retorna arquivos imediatos da pasta fornecida, com filtro opcional por extensão.

        Args:
            caminho_da_pasta: Caminho da pasta a ser lida.
            extensao_buscada: Extensão para filtrar os arquivos, ex: ".txt"

        Returns:
            Lista de objetos `Arquivo` representando arquivos encontrados.
        """
        objeto_pasta = Pasta(caminho=caminho_da_pasta)
        arquivos: list[Arquivo] = [
            Arquivo(caminho=arquivo.caminho_absoluto)
            for arquivo in objeto_pasta.conteudo_listado
            if arquivo.retornar_o_tipo.value == "Arquivo"
        ]
        if extensao_buscada:
            return [
                arquivo
                for arquivo in arquivos
                if arquivo.extensao_legivel == extensao_buscada
            ]
        return arquivos
