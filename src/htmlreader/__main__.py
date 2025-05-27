import argparse
from htmlreader.backend.cli import run_cli
from htmlreader.frontend.gui import run_gui

def main():
    parser = argparse.ArgumentParser(
        description="HTMLReader – escolha modo CLI ou GUI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["cli", "gui"],
        default="cli",
        help="Modo de execução: 'cli' para terminal, 'gui' para interface gráfica"
    )
    args = parser.parse_args()

    if args.mode == "cli":
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
