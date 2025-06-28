"""
Funções utilitárias para formatação de dados relacionados a arquivos e pastas.

Inclui:
- Conversão de tamanhos em bytes para formatos legíveis
- Formatação de datas
- Interpretação de extensões
- Representação textual de valores booleanos
"""

from datetime import datetime


def formatar_arquivo_tamanho_legivel(tamanho_bytes: int | float) -> str:
    """
    Converte bytes para uma representação legível (B, KB, MB, etc.).

    Args:
        tamanho_bytes (int | float): Valor em bytes.

    Returns:
        str: Representação formatada como string.
    """
    if tamanho_bytes <= 0:
        return "0.00 B"

    unidades: list[str] = ["B", "KB", "MB", "GB", "TB"]
    tamanho_float = float(tamanho_bytes)
    unidade_index = 0

    while tamanho_float >= 1024 and unidade_index < len(unidades) - 1:
        tamanho_float /= 1024
        unidade_index += 1

    return f"{tamanho_float:.2f} {unidades[unidade_index]}"


def formatar_arquivo_data_para_string(float_data_e_hora: float) -> str:
    """
    Converte um timestamp float para o padrão brasileiro 'dd/mm/aaaa HH:MM:SS'.

    Args:
        float_data_e_hora (float): Timestamp a ser formatado.

    Returns:
        str: Data formatada.
    """
    data_e_hora: datetime = datetime.fromtimestamp(timestamp=float_data_e_hora)
    return data_e_hora.strftime("%d/%m/%Y %H:%M:%S")


def formatar_arquivo_obter_extensao_legivel(extensao_arquivo: str) -> str:
    """
    Converte uma extensão de arquivo para uma representação textual legível.

    Args:
        extensao_arquivo (str): Extensão do arquivo (com ou sem ponto).

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
    extensao_normalizada: str = extensao_arquivo.lower().strip()
    if not extensao_normalizada.startswith("."):
        extensao_normalizada: str = f".{extensao_normalizada}"

    return mapa.get(extensao_normalizada, extensao_normalizada.strip(".").upper())


def formatar_arquivo_valor_booleano(valor) -> str:
    """
    Converte valor booleano (ou truthy/falsy) para texto 'Sim' ou 'Não'.

    Args:
        valor: Valor a ser interpretado como booleano.

    Returns:
        str: Texto correspondente.
    """
    return "Sim" if bool(valor) else "Não"
