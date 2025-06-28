"""
Script de pré-configuração para o Makefile do HTMLReader.

Este script garante que o diretório de logs '.logs_makefile' exista antes da execução
das demais etapas do pipeline de automação. Pode ser chamado diretamente ou via Makefile.
"""

import os


def criar_logs_dir() -> None:
    """
    Cria o diretório '.logs_makefile' caso ele não exista.

    Exibe uma mensagem indicando se o diretório foi criado ou já existia.
    """
    logs_path = ".logs_makefile"
    if not os.path.exists(path=logs_path):
        os.makedirs(name=logs_path)
        print(f"🗂️  Diretório '{logs_path}' criado.")
    else:
        print(f"📁 Diretório '{logs_path}' já existe.")


if __name__ == "__main__":
    print("🚀 Pré-configuração iniciada.")
    criar_logs_dir()
