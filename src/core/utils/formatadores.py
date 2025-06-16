"""
Funções auxiliares para formatação de dados da classe Pasta.
"""

from datetime import datetime


def converter_bytes_em_tamanho_legivel(tamanho_bytes: int) -> str:
    """Converte um valor em bytes para um formato de tamanho de arquivo legível.

    Percorre as unidades de medida (B, KB, MB, GB, TB), dividindo o valor
    por 1024 a cada iteração até encontrar a unidade apropriada.

    Args:
        tamanho_bytes (int): O tamanho em bytes a ser convertido.

    Returns:
        str: Uma string formatada representando o tamanho com duas casas
             decimais e a unidade correspondente (e.g., "1.50 MB").
    """
    unidades: list[str] = ["B", "KB", "MB", "GB", "TB"]
    tamanho = float(tamanho_bytes)
    unidade_index = 0

    while tamanho >= 1024 and unidade_index < len(unidades) - 1:
        tamanho /= 1024
        unidade_index += 1

    return f"{tamanho:.2f} {unidades[unidade_index]}"


def formatar_data_para_string(data_e_hora: datetime) -> str:
    """Formata um objeto datetime para uma string no formato 'dd/mm/AAAA HH:MM:SS'.

    Args:
        data (datetime): O objeto datetime a ser formatado.

    Returns:
        str: A data e hora formatadas como uma string.
    """
    return data_e_hora.strftime("%d/%m/%Y %H:%M:%S")
