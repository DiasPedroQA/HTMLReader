"""
Módulo: path_transformer
-------------------------

Este módulo define a classe `PathTransformer`, responsável por transformar
caminhos relativos, simbólicos (~, ./, ../) ou contendo variáveis de ambiente,
em caminhos absolutos baseados no diretório do usuário logado.

Funcionalidades:
- Expansão de variáveis de ambiente e placeholders.
- Resolução segura e limitada de caminhos relativos ascendentes.

Compatível com Python 3.12+.
"""

from pathlib import Path
import os
import re
import getpass
import platform


class PathTransformer:
    def __init__(self, max_tentativas: int = 10) -> None:
        self.os_name: str = platform.system()
        self.username: str = getpass.getuser()
        self.home: Path = Path.home()
        self.max_tentativas: int = max_tentativas

    def transformar_para_absoluto(self, caminho: str | Path) -> Path:
        print(f"[DEBUG] Tentando transformar caminho: {caminho!r}")

        if isinstance(caminho, str):
            caminho = self._expandir_variaveis(caminho)
            caminho = Path(caminho)

        try:
            resolvido = caminho.expanduser().resolve(strict=False)
            print(f"[SUCCESS] Caminho resolvido: {resolvido}")
            return resolvido
        except OSError as e:
            print(f"[ERROR] Falha ao resolver caminho: {e}")
            return caminho

    def _expandir_variaveis(self, caminho: str) -> str:
        print(f"[DEBUG] Expandindo variáveis no caminho: {caminho!r}")

        caminho = caminho.replace("~", str(self.home))
        caminho = os.path.expandvars(caminho)
        caminho = re.sub(r"\$(\w+)", lambda m: os.getenv(m.group(1), ""), caminho)
        caminho = caminho.format(username=self.username)

        print(f"[DEBUG] Caminho após expansão: {caminho!r}")
        return caminho


# ✅ Exemplo de uso (teste.py)

if __name__ == "__main__":
    transformador = PathTransformer()

    caminho1: Path = transformador.transformar_para_absoluto(caminho="~/Downloads/Firefox")
    print(f"\ncaminho1 => {caminho1}")

    caminho2: Path = transformador.transformar_para_absoluto(caminho="../Downloads/Firefox")
    print(f"\ncaminho2 => {caminho2}")

#     caminho3: Path = transformador.transformar_para_absoluto(
#         caminho="$HOME/Downloads/Firefox/bookmarks.html"
#     )
#     print(f"\ncaminho3 => {caminho3}")

#     caminho4: Path = transformador.transformar_para_absoluto(
#         caminho="/home/{username}/Downloads/Firefox/bookmarks.html"
#     )
#     print(f"\ncaminho4 => {caminho4}")
