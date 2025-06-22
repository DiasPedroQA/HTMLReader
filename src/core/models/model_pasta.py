"""
Modelos relacionados à manipulação de diretórios no sistema de arquivos.

Define a classe `Pasta`, especialização de `CaminhoBase`, com operações comuns como:
- Criação condicional
- Listagem e análise de conteúdo
- Cálculo de tamanho
- Contagem por extensão
- Detecção de arquivos ocultos
"""

from collections import Counter
from pathlib import Path

from core.models.model_caminho_base import CaminhoBase
from core.utils.formatadores import converter_bytes_em_tamanho_legivel, formatar_data_para_string, formatar_nome_arquivo


class Pasta(CaminhoBase):
    """Representa um diretório e fornece métodos de inspeção e manipulação."""

    @property
    def itens_diretos(self) -> list[CaminhoBase]:
        """Retorna os itens diretamente contidos no diretório."""
        if not self.caminho_existe or not self._path.is_dir():
            print(f"Caminho {self.caminho_existe} não existe ou não é uma pasta")
            return []
        return [CaminhoBase(caminho=entrada) for entrada in self._path.iterdir()]

    @property
    def nome(self) -> str:
        """Retorna o nome do diretório, formatado."""
        return formatar_nome_arquivo(nome=self._path.stem)

    @property
    def total_arquivos(self) -> int:
        """Conta quantos arquivos existem diretamente no diretório."""
        return sum(1 for item in self.itens_diretos if item.retornar_o_tipo == "Arquivo")

    @property
    def total_subpastas(self) -> int:
        """Conta quantas subpastas existem diretamente no diretório."""
        return sum(1 for item in self.itens_diretos if item.retornar_o_tipo == "Pasta")

    @property
    def possui_ocultos(self) -> bool:
        """Verifica se há arquivos ou pastas ocultos (que começam com ponto)."""
        return any(item.nome_caminho.startswith(".") for item in self.itens_diretos)

    @property
    def data_modificacao_formatada(self) -> str | None:
        """Retorna a data da última modificação no diretório, formatada."""
        return formatar_data_para_string(data_e_hora=self.data_modificacao) if self.data_modificacao else None

    @property
    def tamanho_formatado(self) -> str:
        """Retorna o tamanho total do diretório em formato legível (KB, MB, etc)."""
        return converter_bytes_em_tamanho_legivel(tamanho_bytes=self.calcular_tamanho_total())

    def listar_conteudo_recursivo(self) -> list[CaminhoBase]:
        """Lista todos os arquivos e subpastas contidos no diretório, de forma recursiva."""
        if not self.caminho_existe or not self._path.is_dir():
            return []
        return [CaminhoBase(caminho=item) for item in self._path.rglob(pattern="*")]

    def listar_ocultos(self) -> list[Path]:
        """Retorna os caminhos dos itens ocultos diretamente contidos no diretório."""
        return [item.caminho_absoluto for item in self.itens_diretos if item.nome_caminho.startswith(".")]

    def calcular_tamanho_total(self) -> int:
        """Soma os tamanhos de todos os arquivos contidos no diretório e subpastas."""
        if not self.caminho_existe:
            return 0

        total_bytes = 0
        for arquivo in self._path.rglob(pattern="*"):
            if arquivo.is_file():
                try:
                    total_bytes += arquivo.stat().st_size
                except OSError:
                    continue
        return total_bytes

    def contar_extensoes(self) -> dict[str, int]:
        """
        Conta a quantidade de arquivos por extensão no diretório e subpastas.

        Returns:
            dict[str, int]: Chaves são extensões, valores são contagens.
        """
        if not self.caminho_existe:
            return {}

        extensoes: list[str] = [
            arquivo.suffix.lower() for arquivo in self._path.rglob(pattern="*") if arquivo.is_file() and arquivo.suffix
        ]
        return dict(Counter(extensoes))
