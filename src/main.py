"""
Ponto de entrada principal do HTMLReader.

Este módulo integra backend e frontend, permitindo inicialização via CLI, GUI ou API.
"""

import sys
from typing import NoReturn


def start_gui() -> None:
    """
    Inicializa a interface gráfica (Tkinter).
    """
    # from htmlreader.interfaces.gui import start_app
    # start_app()
    print("Inicializando interface gráfica... (implemente em interfaces/gui)")


def start_cli() -> None:
    """
    Inicializa a interface de linha de comando.
    """
    # from htmlreader.interfaces.cli import main_cli
    # main_cli()
    print("Inicializando CLI... (implemente em interfaces/cli)")


def start_api() -> None:
    """
    Inicializa a API (ex: FastAPI/Flask).
    """
    # from htmlreader.interfaces.api import start_api
    # start_api()
    print("Inicializando API... (implemente em interfaces/api)")


def main(mode: str = "gui") -> NoReturn:
    """
    Função principal para gerenciar o modo de inicialização do app.

    Args:
        mode (str): Modo de execução ('gui', 'cli', 'api').
    """
    if mode == "gui":
        start_gui()
    elif mode == "cli":
        start_cli()
    elif mode == "api":
        start_api()
    else:
        print(f"Modo '{mode}' não reconhecido. Use 'gui', 'cli' ou 'api'.")

    sys.exit(0)


if __name__ == "__main__":
    mode_atual = sys.argv[1] if len(sys.argv) > 1 else "gui"
    main(mode_atual)
