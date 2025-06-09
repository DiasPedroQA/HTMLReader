from typing import Literal
from pydantic import BaseModel


class Arquivo(BaseModel):
    nome: str
    caminho: str
    tipo: Literal["html", "outro"]
    tamanho: int


# from pathlib import Path
# from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr


# class Arquivo(CaminhoNormal):
#     """
#     Representa um arquivo válido no sistema de arquivos.

#     Atributos:
#         caminho_absoluto: Caminho absoluto resolvido.
#         nome_arquivo: Nome do arquivo (com extensão).
#         extensao: Extensão do arquivo (ex: .txt).
#         conteudo_arquivo: Conteúdo textual, se legível.
#         tamanho_bytes: Tamanho em bytes.
#         criado_em_timestamp: Timestamp de criação.
#         modificado_em_timestamp: Timestamp de modificação.
#         pasta_atual: Caminho da pasta onde o arquivo está localizado.
#     """

#     caminho_absoluto: Path
#     nome_arquivo: StrictStr
#     extensao: StrictStr | None = None
#     conteudo_arquivo: StrictStr | None = None
#     tamanho_bytes: StrictInt | None = None
#     criado_em_timestamp: StrictFloat | None = None
#     modificado_em_timestamp: StrictFloat | None = None
#     pasta_atual: Path


# class Pasta(CaminhoNormal):
#     """
#     Representa uma pasta válida no sistema de arquivos.

#     Atributos:
#         caminho_absoluto: Caminho absoluto resolvido.
#         arquivos_na_pasta: Lista de nomes de arquivos na pasta.
#         subpastas: Lista de nomes de subpastas.
#     """

#     caminho_absoluto: Path
#     arquivos_na_pasta: list[Path] | None = None
#     subpastas: list[Path] | None = None
