"""
Interface de linha de comando (CLI) do HTMLReader.

Permite visualizar o conteúdo de pastas/arquivos e processar arquivos via terminal,
utilizando os serviços de visor e processador.
"""

import argparse
from pathlib import Path
from src.htmlreader.core.services import visor_service, processador_service
from src.htmlreader.core.models.visor_models import FiltroVisor
from src.htmlreader.core.models.processador_models import LoteDeArquivos


def main():
    """
    Função principal da CLI. Interpreta argumentos e
    executa comandos de visualização ou processamento.
    """
    parser = argparse.ArgumentParser(description="HTMLReader CLI")
    subparsers = parser.add_subparsers(dest="comando")

    # Subcomando: visor
    visor_parser = subparsers.add_parser("visor", help="Visualizar pasta ou arquivo")
    visor_parser.add_argument("path", type=Path)
    visor_parser.add_argument("--filtro-ext", nargs="*", help="Ex: .html .txt")
    visor_parser.add_argument(
        "--tipo", choices=["arquivo", "pasta"], help="Filtrar por tipo"
    )

    # Subcomando: processar
    proc_parser = subparsers.add_parser("processar", help="Processar arquivos")
    proc_parser.add_argument("arquivos", nargs="+", type=Path)
    proc_parser.add_argument("--saida", default=".json")

    args = parser.parse_args()

    if args.comando == "visor":
        # Visualiza o conteúdo de uma pasta ou exibe prévia de um arquivo.
        caminho = args.path
        if caminho.is_dir():
            filtros = FiltroVisor(extensoes=args.filtro_ext, tipo=args.tipo)
            resultado = visor_service.listar_conteudo(caminho, filtros)
            for item in resultado.itens:
                print(f"[{item.tipo.upper()}] {item.path}")
        elif caminho.is_file():
            previa = visor_service.obter_previa(caminho)
            print(f"Arquivo: {previa.nome} ({previa.extensao})")
            print(f"Tamanho: {previa.tamanho_bytes} bytes")
            print("Prévia:")
            print("\n".join(previa.linhas))
        else:
            print("Caminho inválido.")

    elif args.comando == "processar":
        # Processa um ou mais arquivos, gerando arquivos de saída.
        lote = LoteDeArquivos(arquivos=[{"path": p} for p in args.arquivos])
        resultados = processador_service.processar_em_lote(lote, args.saida)
        for res in resultados:
            status = "OK" if res.sucesso else "FALHA"
            print(f"{status} - {res.entrada} → {res.saida} | {res.mensagem}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
