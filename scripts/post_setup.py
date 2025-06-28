"""
Script de pós-configuração para o Makefile do HTMLReader.

Este script exibe a estrutura de diretórios do projeto após a configuração,
ajudando na verificação visual do ambiente criado.
Pode ser chamado diretamente ou via Makefile.
"""

import os


def mostrar_estrutura() -> None:
    """
    Exibe a estrutura de diretórios e arquivos do projeto no terminal.
    """
    print("\n📂 Estrutura atual de diretórios do projeto:")
    for root, _, files in os.walk(".", topdown=True):
        level: int = root.replace(os.path.dirname("."), "").count(os.sep)
        indent: str = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{indent}  {f}")


if __name__ == "__main__":
    print("🎯 Pós-configuração iniciada.")
    mostrar_estrutura()
