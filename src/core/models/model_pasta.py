"""
Módulo de representação e manipulação de diretórios no sistema de arquivos.

Este módulo define a classe `Pasta`, uma especialização de `CaminhoBase`, que fornece
operações úteis relacionadas a diretórios, incluindo:

- Criação condicional de pastas
- Listagem de conteúdo (direta e recursiva)
- Cálculo do tamanho total de arquivos contidos
- Contagem de arquivos e sub_pastas
- Identificação de arquivos ocultos
- Análise de distribuição por extensão de arquivos

Classes:
    Pasta: Representa um diretório e fornece métodos de inspeção e manipulação.
"""

from pathlib import Path
from collections import Counter

from core.models.model_caminho_base import CaminhoBase
from core.services.formatadores import (
    converter_bytes_em_tamanho_legivel,
    formatar_data_para_string,
    formatar_nome_arquivo,
)


class Pasta(CaminhoBase):
    """
    Classe que representa uma pasta (diretório) no sistema de arquivos.

    Herda de CaminhoBase e oferece métodos específicos para manipulação e inspeção
    do conteúdo de diretórios.

    Métodos:
        conteudo_listado: Retorna os itens diretamente contidos na pasta.
        nome_pasta: Retorna o nome da pasta (sem caminho).
        quantidade_arquivos: Conta arquivos diretamente contidos.
        quantidade_pastas: Conta sub_pastas diretamente contidas.
        existe_arquivo_oculto: Verifica a existência de arquivos ocultos.
        data_modificacao_legivel: Retorna a data da última modificação formatada.
        coletar_itens_recursivamente: Coleta todo conteúdo recursivamente.
        coletar_itens_ocultos: Coleta dos nomes dos arquivos e pastas ocultos.
        calcular_tamanho_total: Soma o tamanho de todos os arquivos contidos.
        tamanho_total_legivel: Retorna o tamanho em formato legível.
        contar_por_extensao: Conta arquivos por tipo de extensão.
    """

    @property
    def conteudo_listado(self) -> list[CaminhoBase]:
        """
        Coleta todos os arquivos e sub_pastas diretamente contidos na pasta.

        Returns:
            list[CaminhoBase]: Lista de itens no diretório (não recursiva).
        """
        if not self.caminho_existe or not self._path.is_dir():
            return []
        return [
            CaminhoBase(caminho=caminho_pasta) for caminho_pasta in self._path.iterdir()
        ]

    @property
    def nome_pasta(self) -> str:
        """
        Retorna o nome da pasta (sem caminho e sem extensão).

        Returns:
            str: Nome da pasta.
        """
        return formatar_nome_arquivo(nome=self._path.stem)

    @property
    def quantidade_arquivos(self) -> int:
        """
        Conta quantos arquivos existem diretamente na pasta.

        Returns:
            int: Quantidade de arquivos.
        """
        return len([
            p for p in self.conteudo_listado if p.retornar_o_tipo.value == "Arquivo"
        ])

    @property
    def quantidade_pastas(self) -> int:
        """
        Conta quantas sub_pastas existem diretamente na pasta.

        Returns:
            int: Quantidade de subdiretórios.
        """
        return len([
            pasta
            for pasta in self.conteudo_listado
            if pasta.retornar_o_tipo.value == "Pasta"
        ])

    @property
    def existe_arquivo_oculto(self) -> bool:
        """
        Verifica se há arquivos ou pastas ocultos (cujo nome começa com ponto).

        Returns:
            bool: True se houver pelo menos um item oculto, False caso contrário.
        """
        return any(p.nome_caminho.startswith(".") for p in self.conteudo_listado)

    @property
    def data_modificacao_legivel(self) -> str | None:
        """
        Retorna a data da última modificação da pasta, em formato legível.

        Returns:
            str | None: Data formatada como string, ou None se indisponível.
        """
        if self.data_modificacao is None:
            return None
        return formatar_data_para_string(data_e_hora=self.data_modificacao)

    def coletar_itens_recursivamente(self) -> list[CaminhoBase]:
        """
        ê todos os arquivos e sub_pastas contidos numa pasta, de forma recursiva.

        Returns:
            list[CaminhoBase]: Lista completa de caminhos encontrados na pasta e sub_pastas.
        """
        if not self.caminho_existe or not self._path.is_dir():
            return []
        return [CaminhoBase(caminho=item) for item in self._path.rglob("*")]

    def coletar_itens_ocultos(self) -> list[Path]:
        """
        ê os nomes dos arquivos e pastas ocultos diretamente contidos.

        Returns:
            list[str]: Coleta dos nomes dos itens ocultos.
        """
        return [
            p.caminho_absoluto
            for p in self.conteudo_listado
            if p.nome_caminho.startswith(".")
        ]

    def calcular_tamanho_total(self) -> int:
        """
        Calcula o tamanho total da pasta somando os tamanhos dos arquivos contidos.

        Returns:
            int: Tamanho total em bytes.
        """
        if not self.caminho_existe:
            return 0

        total = 0
        for arquivo in self._path.rglob(pattern="*"):
            if arquivo.is_file():
                try:
                    total += arquivo.stat().st_size
                except OSError:
                    continue
        return total

    @property
    def tamanho_total_legivel(self) -> str:
        """
        Retorna o tamanho total da pasta em formato legível (KB, MB, etc).

        Returns:
            str: Tamanho formatado, ex: "12.3 MB".
        """
        return converter_bytes_em_tamanho_legivel(
            tamanho_bytes=self.calcular_tamanho_total()
        )

    def contar_por_extensao(self) -> dict[str, int]:
        """
        Conta quantos arquivos existem por tipo de extensão (recursivamente).

        Returns:
            dict[str, int]: Dicionário onde as chaves são extensões e os valores suas contagens.
        """
        if not self.caminho_existe:
            return {}

        extensoes: list[str] = [
            p.suffix.lower() for p in self._path.rglob(pattern="*") if p.is_file() and p.suffix
        ]
        return dict(Counter(extensoes))
