"""
Interface de linha de comando (CLI) do HTMLReader:
– exibe informações do OS
– analisa caminhos
"""

import sys
from htmlreader.core.utils.system_utils import get_os_info, analyze_path


def run_cli() -> None:
    """
    Executa a interface de terminal:
    1) Mostra informações do sistema operacional.
    2) Analisa um caminho de arquivo ou diretório informado pelo usuário ou via argumento.
    """
    # 1) OS Info
    print("=== Informações do Sistema ===")
    for k, v in get_os_info().items():
        print(f"{k:>10}: {v}")
    print()

    # Permite passar o caminho como argumento ou via input
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input(
            "Digite um caminho de arquivo ou diretório para analisar: "
        ).strip()

    # 2) Path Analyzer
    try:
        path_info: dict[str, str] = analyze_path(path)
        print("\n=== Resultado da Análise de Caminho ===")
        for k, v in path_info.items():
            print(f"{k:>16}: {str(v)}")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Erro ao analisar o caminho: {e}")
    print()


if __name__ == "__main__":
    run_cli()
