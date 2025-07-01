# scripts/gerar_gitignore.py

import requests
from pathlib import Path

# Ambientes que queremos incluir
TEMPLATES: list[str] = [
    "Python",
    "Linux",
    "macOS",
    "Windows",
    "VisualStudioCode",
    "JupyterNotebooks",
    "Docker",
]

DESTINO = Path(".gitignore")


def gerar_gitignore() -> None:
    conteudo_final: list[str] = []

    for template in TEMPLATES:
        url: str = f"https://raw.githubusercontent.com/github/gitignore/main/{template}.gitignore"
        resposta: requests.Response = requests.get(url=url)
        if resposta.status_code == 200:
            conteudo_final.append(f"# === {template} ===\n{resposta.text.strip()}\n")
        else:
            print(f"⚠️ Falha ao baixar: {template}")

    DESTINO.write_text("\n\n".join(conteudo_final), encoding="utf-8")
    print("✅ .gitignore gerado com sucesso.")


if __name__ == "__main__":
    gerar_gitignore()
