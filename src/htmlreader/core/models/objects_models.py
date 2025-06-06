"""
Modelos de dados relacionados ao sistema de arquivos.

Este módulo define estruturas de dados que representam caminhos válidos e inválidos
no sistema de arquivos, bem como entidades específicas para arquivos e diretórios.
Esses modelos são utilizados como contratos entre as camadas de serviço e as interfaces
(API, CLI, GUI), mantendo a integridade e previsibilidade das informações trafegadas.
"""
from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr


class CaminhoBruto(BaseModel):
    """
    Representa um caminho em formato de texto recebido como entrada pelo sistema.

    Atributos:
        caminho_original (str): Caminho original fornecido pelo usuário.
    """

    caminho_original: StrictStr


class CaminhoValido(CaminhoBruto):
    """
    Representa um caminho validado e resolvido com sucesso no sistema de arquivos.

    Atributos:
        caminho_absoluto (str): Caminho absoluto resolvido, pronto para uso interno.
    """

    caminho_absoluto: StrictStr


class CaminhoInvalido(BaseModel):
    """
    Representa um caminho considerado inválido, junto com o motivo da invalidação.

    Atributos:
        caminho_invalido (str): Caminho que falhou na validação.
        motivo (str): Descrição do motivo da falha.
    """

    caminho_invalido: StrictStr
    motivo: StrictStr


class Arquivo(CaminhoValido):
    """
    Representa um arquivo existente no sistema de arquivos, com informações opcionais.

    Atributos:
        conteudo_arquivo (str | None): Conteúdo textual do arquivo.
        tamanho_bytes (int | None): Tamanho do arquivo em bytes.
        modificado_em_timestamp (float | None): Timestamp da última modificação.
        criado_em_timestamp (float | None): Timestamp de criação.
        pasta_atual (str | None): Caminho da pasta em que o arquivo está.
    """

    conteudo_arquivo: StrictStr | None = None
    tamanho_bytes: StrictInt | None = None
    modificado_em_timestamp: StrictFloat | None = None
    criado_em_timestamp: StrictFloat | None = None
    pasta_atual: StrictStr | None = None


class Pasta(CaminhoValido):
    """
    Representa um diretório existente no sistema de arquivos, com listagens opcionais.

    Atributos:
        arquivos_na_pasta (list[str] | None): Lista com os nomes dos arquivos contidos na pasta.
        subpastas (list[str] | None): Lista com os nomes das subpastas contidas na pasta.
    """

    arquivos_na_pasta: list[StrictStr] | None = None
    subpastas: list[StrictStr] | None = None
