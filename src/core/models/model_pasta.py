"""
Módulo de representação e manipulação de diretórios no sistema de arquivos.

Este módulo define a classe `Pasta`, uma especialização de `CaminhoBase`, que fornece
operações úteis relacionadas a diretórios, incluindo:

- Criação condicional de pastas
- Listagem de conteúdo (direta e recursiva)
- Cálculo do tamanho total de arquivos contidos
- Contagem de arquivos e subpastas
- Identificação de arquivos ocultos
- Análise de distribuição por extensão de arquivos

Classes:
    Pasta: Representa um diretório e fornece métodos de inspeção e manipulação.
"""

from pathlib import Path
from collections import Counter

from core.models.model_caminho_base import CaminhoBase
from core.utils.formatadores import (
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
        quantidade_pastas: Conta subpastas diretamente contidas.
        existe_arquivo_oculto: Verifica a existência de arquivos ocultos.
        data_modificacao_formatada: Retorna a data da última modificação formatada.
        listar_recursivo: Lista todo conteúdo recursivamente.
        listar_ocultos: Lista nomes dos arquivos e pastas ocultos.
        calcular_tamanho_total: Soma o tamanho de todos os arquivos contidos.
        tamanho_total_legivel: Retorna o tamanho em formato legível.
        contar_por_extensao: Conta arquivos por tipo de extensão.
    """

    @property
    def conteudo_listado(self) -> list[Path]:
        """
        Lista todos os arquivos e subpastas diretamente contidos na pasta.

        Returns:
            list[Path]: Lista de entradas no diretório (não recursiva).
        """
        if not self.caminho_existe or not self._path.is_dir():
            return []
        return list(self._path.iterdir())

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
        return len([p for p in self.conteudo_listado if p.is_file()])

    @property
    def quantidade_pastas(self) -> int:
        """
        Conta quantas subpastas existem diretamente na pasta.

        Returns:
            int: Quantidade de subdiretórios.
        """
        return len([p for p in self.conteudo_listado if p.is_dir()])

    @property
    def existe_arquivo_oculto(self) -> bool:
        """
        Verifica se há arquivos ou pastas ocultos (cujo nome começa com ponto).

        Returns:
            bool: True se houver pelo menos um item oculto, False caso contrário.
        """
        return any(p.name.startswith(".") for p in self.conteudo_listado)

    @property
    def data_modificacao_formatada(self) -> str | None:
        """
        Retorna a data da última modificação da pasta, em formato legível.

        Returns:
            str | None: Data formatada como string, ou None se indisponível.
        """
        if self.data_modificacao is None:
            return None
        return formatar_data_para_string(data_e_hora=self.data_modificacao)

    def criar_se_nao_existir(self) -> bool:
        """
        Cria a pasta se ela ainda não existir.

        Returns:
            bool: True se criada com sucesso, False se já existia.
        """
        if not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)
            return True
        return False

    def listar_recursivo(self) -> list[Path]:
        """
        Lista todos os arquivos e subpastas contidos na pasta, de forma recursiva.

        Returns:
            list[Path]: Lista completa de caminhos encontrados na pasta e subpastas.
        """
        if not self.caminho_existe or not self._path.is_dir():
            return []
        return list(self._path.rglob("*"))

    def listar_ocultos(self) -> list[str]:
        """
        Lista os nomes dos arquivos e pastas ocultos diretamente contidos.

        Returns:
            list[str]: Lista de nomes dos itens ocultos.
        """
        return [p.name for p in self.conteudo_listado if p.name.startswith(".")]

    def calcular_tamanho_total(self) -> int:
        """
        Calcula o tamanho total da pasta somando os tamanhos dos arquivos contidos.

        Returns:
            int: Tamanho total em bytes.
        """
        if not self.caminho_existe:
            return 0

        total = 0
        for arquivo in self._path.rglob("*"):
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
            p.suffix.lower() for p in self._path.rglob("*") if p.is_file() and p.suffix
        ]
        return dict(Counter(extensoes))
