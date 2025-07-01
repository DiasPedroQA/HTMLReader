"""
Modelo de dados para informações do sistema operacional.

Este módulo define a estrutura `SistemaInfo`, utilizada para representar e transportar
informações coletadas do ambiente do sistema operacional, como nome, versão, arquitetura,
separadores de diretório e tempo de atividade da máquina.

O modelo é utilizado principalmente pelo `SistemaController`, e pode ser exposto via API.
"""

from pydantic import BaseModel


class SistemaInfo(BaseModel):
    """
    Modelo de dados que representa o estado atual do sistema operacional.

    Atributos:
        sistema_operacional: Nome do sistema operacional (ex: 'Linux', 'Windows', 'Darwin').
        versao: Versão do sistema operacional.
        arquitetura: Arquitetura da máquina (ex: 'x86_64', 'arm64').
        nome_maquina: Nome do host ou máquina atual.
        separador_diretorio: Caractere separador de diretório (ex: '/', '\\').
        diretorio_atual: Caminho absoluto do diretório onde o processo está sendo executado.
        raiz_sistema_arquivos: Diretório raiz do sistema de arquivos (ex: '/', 'C:\\').
        codificacao_padrao: Codificação padrão do sistema (ex: 'utf-8').
        tempo_desde_boot: Tempo de atividade da máquina desde o último boot, em string legível.
        versao_api: Versão da API que está retornando os dados.
        diretorio_usuario: Caminho absoluto para o diretório inicial do usuário (ex: '/home/usuario', 'C:\\Users\\usuario').
    """

    sistema_operacional: str
    versao: str
    arquitetura: str
    nome_maquina: str
    separador_diretorio: str
    diretorio_atual: str
    raiz_sistema_arquivos: str
    codificacao_padrao: str
    tempo_desde_boot: str
    versao_api: str
    diretorio_usuario: str
