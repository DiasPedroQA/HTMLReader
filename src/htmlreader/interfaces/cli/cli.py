"""
Interface de linha de comando (CLI) do HTMLReader:
– exibe informações do OS
– analisa caminhos
"""

from htmlreader.backend.parser import get_os_info, analyze_path

def run_cli() -> None:
    """
    Executa a interface de terminal completa:
    1) mostra infos do OS
    2) analisa caminho
    """

    # 1) OS Info
    print("=== Informações do Sistema ===")
    for k, v in get_os_info().items():
        print(f"{k:>10}: {v}")
    print()

    # 2) Path Analyzer
    path = input("Digite um caminho de arquivo ou diretório para analisar: ").strip()
    path_info = analyze_path(path)
    print("\n=== Resultado da Análise de Caminho ===")
    for k, v in path_info.items():
        print(f"{k:>12}: {v}")
    print()


if __name__ == "__main__":
    run_cli()
