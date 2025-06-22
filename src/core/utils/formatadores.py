"""
Funções utilitárias para formatação de dados relacionados a arquivos e pastas.

Inclui:
- Conversão de tamanhos em bytes para formatos legíveis
- Formatação de datas
- Interpretação de extensões
- Representação textual de valores booleanos
- Truncamento seguro de nomes de arquivos
"""

from datetime import datetime


def converter_bytes_em_tamanho_legivel(tamanho_bytes: int) -> str:
    """
    Converte bytes para uma representação legível (B, KB, MB, etc.).

    Args:
        tamanho_bytes (int): Valor em bytes.

    Returns:
        str: Representação formatada como string.
    """
    if tamanho_bytes <= 0:
        return "0.00 B"

    unidades: list[str] = ["B", "KB", "MB", "GB", "TB"]
    tamanho = float(tamanho_bytes)
    unidade_index = 0

    while tamanho >= 1024 and unidade_index < len(unidades) - 1:
        tamanho /= 1024
        unidade_index += 1

    return f"{tamanho:.2f} {unidades[unidade_index]}"


def formatar_data_para_string(data_e_hora: datetime) -> str:
    """
    Formata um objeto datetime para o padrão brasileiro 'dd/mm/aaaa HH:MM:SS'.

    Args:
        data_e_hora (datetime): Data a ser formatada.

    Returns:
        str: Data formatada.
    """
    return data_e_hora.strftime(format="%d/%m/%Y %H:%M:%S")


def obter_extensao_legivel(extensao: str) -> str:
    """
    Converte uma extensão de arquivo para uma representação textual legível.

    Args:
        extensao (str): Extensão do arquivo (com ou sem ponto).

    Returns:
        str: Nome legível da extensão.
    """
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
    extensao_normalizada: str = extensao.lower().strip()
    if not extensao_normalizada.startswith("."):
        extensao_normalizada: str = f".{extensao_normalizada}"

    return mapa.get(extensao_normalizada, extensao_normalizada.strip(".").upper())


def formatar_booleano(valor: bool) -> str:
    """
    Converte valor booleano para texto 'Sim' ou 'Não'.

    Args:
        valor (bool): Valor booleano.

    Returns:
        str: Texto correspondente.
    """
    return "Sim" if valor else "Não"


def formatar_nome_arquivo(nome: str, limite: int = 50) -> str:
    """
    Trunca nomes longos de arquivo, mantendo sufixo "...".

    Args:
        nome (str): Nome original.
        limite (int): Tamanho máximo permitido.

    Returns:
        str: Nome truncado, se necessário.
    """
    if not nome:
        return ""
    if limite < 4:
        return "..."
    return nome if len(nome) <= limite else nome[: limite - 3] + "..."
