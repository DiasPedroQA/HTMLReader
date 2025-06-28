"""
Módulo para representação de diretórios com navegação e filtragem de arquivos.

Define a classe `Pasta`, que representa diretórios com funcionalidades como:
- Listagem de arquivos e subpastas
- Filtros por extensão, nome ou função personalizada
- Cálculo de tamanho total e análise de conteúdo
"""

import os
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

from core.models.model_arquivo import Arquivo


@dataclass
class Pasta:
    """
    Representa um diretório no sistema de arquivos com funcionalidades
    para navegação, busca e análise de arquivos e subdiretórios.

    Atributos:
        caminho (Path): Caminho absoluto ou relativo da pasta.
    """

    caminho: Path

    def validar(self) -> None:
        """
        Verifica se o atributo `caminho` referencia um diretório válido.

        Raises:
            NotADirectoryError: Se `caminho` não for uma pasta válida.
        """
        if not self.caminho.is_dir():
            raise NotADirectoryError(f"{self.caminho} não é um diretório válido.")

    @property
    def arquivos(self) -> Iterator[Arquivo]:
        """
        Itera sobre os arquivos diretos contidos na pasta.

        Yields:
            Arquivo: Instância do model `Arquivo` para cada arquivo encontrado.
        """
        for item in self.caminho.iterdir():
            if item.is_file():
                yield Arquivo(caminho=item)

    @property
    def subpastas(self) -> Iterator["Pasta"]:
        """
        Itera sobre as subpastas diretas da pasta atual.

        Yields:
            Pasta: Instância do model `Pasta` para cada subdiretório encontrado.
        """
        for item in self.caminho.iterdir():
            if item.is_dir():
                yield Pasta(caminho=item)

    def buscar(
        self,
        nome: str | None = None,
        extensao: str | None = None,
        filtro: Callable[[Arquivo], bool] | None = None,
    ) -> Iterator[Arquivo]:
        """
        Busca arquivos dentro da pasta que satisfaçam critérios opcionais.

        Args:
            nome (str | None): Substring a ser buscada no nome do arquivo,
                ignorando maiúsculas/minúsculas. Se None, não filtra por nome.
            extensao (str | None): Extensão do arquivo a ser filtrada. Pode conter
                ou não o ponto inicial (ex: ".py" ou "py"). Se None, não filtra.
            filtro (Callable[[Arquivo], bool] | None): Função personalizada para
                filtrar os arquivos. Recebe um objeto `Arquivo` e retorna bool.
                Se None, não aplica filtro adicional.

        Yields:
            Arquivo: Arquivos que satisfazem todos os critérios especificados.
        """
        ext: str | None = extensao.lower().lstrip(".") if extensao else None
        for arq in self.arquivos:
            if nome and nome.lower() not in arq.nome.lower():
                continue
            if ext and arq.extensao != ext:
                continue
            if filtro and not filtro(arq):
                continue
            yield arq

    def calcular_tamanho_total(self) -> int:
        """
        Calcula o tamanho total, em bytes, de todos os arquivos na pasta,
        considerando também subdiretórios (recursivo).

        Retorna:
            int: Soma do tamanho de todos os arquivos válidos na pasta e subpastas.

        Observações:
            Ignora arquivos que não possam ser acessados (ex: erros de permissão).
        """
        total = 0
        for raiz, _, arquivos in os.walk(self.caminho):
            for arquivo in arquivos:
                try:
                    total += (Path(raiz) / arquivo).stat().st_size
                except OSError:
                    continue
        return total

    def contar_extensoes(self) -> dict[str, int]:
        """
        Conta a ocorrência de cada extensão de arquivo presente na pasta e suas subpastas.

        Retorna:
            dict[str, int]: Dicionário onde as chaves são extensões em minúsculo (ex: ".py")
            e os valores são a quantidade de arquivos com aquela extensão.
        """
        extensoes: list[str] = [
            arq.suffix.lower()
            for arq in self.caminho.rglob(pattern="*")
            if arq.is_file() and arq.suffix
        ]
        return dict(Counter(extensoes))


# def exemplo_pasta() -> None:
#     print("\n🔍 Teste com pasta válida")
#     pasta_atual = Pasta(caminho=Path("../"))

#     try:
#         pasta_atual.validar()
#         print("✔️ Pasta válida.")

#         print("📂 Subpastas:")
#         for sub in pasta_atual.subpastas:
#             print(f"  - {sub.caminho}")

#         print("\n📄 Arquivos:")
#         for arq in pasta_atual.arquivos:
#             print(f"  - {arq.nome}")

#         print("\n🔎 Buscar arquivos '.py':")
#         for arq in pasta_atual.buscar(extensao=".py"):
#             print(f"  - {arq.nome}")

#         print(
#             f"\n📐 Tamanho total da pasta: {pasta_atual.calcular_tamanho_total()} bytes"
#         )

#         print("\n📊 Extensões encontradas:")
#         for ext, count in pasta_atual.contar_extensoes().items():
#             print(f"  - {ext}: {count}")

#     except NotADirectoryError as e:
#         print(f"[ERRO] {e}")

#     print("\n❌ Teste com pasta inexistente")
#     pasta_invalida = Pasta(caminho=Path("caminho/que/nao/existe"))
#     try:
#         pasta_invalida.validar()
#     except NotADirectoryError as e:
#         print(f"[ERRO] {e}")


# if __name__ == "__main__":
#     exemplo_pasta()
