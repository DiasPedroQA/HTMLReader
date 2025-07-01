"""
Script de configuração principal para o Makefile do HTMLReader.

Este script instala as dependências do projeto a partir do arquivo requirements.txt.
Pode ser chamado diretamente ou via Makefile.
"""

import subprocess
import sys


def instalar_dependencias() -> None:
    """
    Instala as dependências listadas em requirements.txt usando pip.

    Em caso de falha, exibe mensagem de erro e encerra o script.
    """
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
            ]
        )
        print("📦 Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError:
        print("❌ Falha ao instalar dependências.")
        sys.exit(1)


if __name__ == "__main__":
    print("🔄 Configuração principal em andamento...")
    instalar_dependencias()
