"""
Funções auxiliares para formatação de dados de arquivos e pastas.
"""

from datetime import datetime


def converter_bytes_em_tamanho_legivel(tamanho_bytes: int) -> str:
    """Converte um valor em bytes para um formato legível."""
    unidades: list[str] = ["B", "KB", "MB", "GB", "TB"]
    tamanho = float(tamanho_bytes)
    unidade_index = 0

    while tamanho >= 1024 and unidade_index < len(unidades) - 1:
        tamanho /= 1024
        unidade_index += 1

    return f"{tamanho:.2f} {unidades[unidade_index]}"


def formatar_data_para_string(data_e_hora: datetime) -> str:
    """Formata datetime para 'dd/mm/aaaa HH:MM:SS'."""
    return data_e_hora.strftime(format="%d/%m/%Y %H:%M:%S")


def obter_extensao_legivel(extensao: str) -> str:
    """Converte extensão técnica para nome amigável."""
    mapa: dict[str, str] = {
        ".txt": "Texto",
        ".md": "Markdown",
        ".json": "JSON",
        ".csv": "Planilha CSV",
        ".py": "Script Python",
        ".xml": "XML",
        ".html": "HTML",
        ".log": "Log",
    }
    return mapa.get(extensao.lower(), extensao.strip(".").upper())


def formatar_booleano(valor: bool) -> str:
    """Converte booleano para 'Sim' ou 'Não'."""
    return "Sim" if valor else "Não"


def formatar_nome_arquivo(nome: str, limite: int = 50) -> str:
    """Trunca nomes longos de arquivo."""
    return nome if len(nome) <= limite else nome[: limite - 3] + "..."
