"""Rotas da API responsáveis por fornecer informações do sistema operacional."""

# from fastapi import APIRouter
# from core.controllers.info_sistema_controller import InfoSistemaController
# from core.models.models_dominio import Pasta
# from core.models.pasta_models import Pasta
# from core.controllers.pasta_controller import PastaController
# from core.controllers.conversao_controller import ConversaoController
# from core.controllers.file_path_controller import listar_arquivos_html
# from core.services.visor_service import ler_conteudo_arquivo
# from core.services.system_info import (
#     obter_infos_sistema,
# )  # crie esse service com PathBuilder, se ainda não existir
# from core.services.visor_service import detalhar_arquivo
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse

# router = APIRouter()
# controller = InfoSistemaController()


# @router.get(path="/sistema/completo")
# def obter_info_sistema() -> dict:
#     """
#     Retorna informações do sistema operacional, usuário logado e
#     representação da pasta home como um dicionário serializável.

#     Returns:
#         dict: Dados do sistema e da pasta home do usuário.
#     """
#     dados: dict = controller.obter_info_sistema()

#     pasta_home: Pasta = dados["home"]

#     return {
#         "usuario": dados["usuario"],
#         "sistema": dados["sistema"],
#         "versao": dados["versao"],
#         "home": {
#             "nome": pasta_home.nome,
#             "caminho": pasta_home.caminho,
#             "tamanho_bytes": pasta_home.tamanho_bytes,
#             "criado_em": pasta_home.criado_em.isoformat(),
#             "modificado_em": pasta_home.modificado_em.isoformat(),
#         },
#     }


# """
# Rotas da API para consulta das informações do sistema operacional
# e usuário logado.
# """

# from fastapi import APIRouter, HTTPException
# from core.models.modelos_api import InfoSistemaOut
# from core.controllers.info_sistema_controller import InfoSistemaController

# router = APIRouter(prefix="/sistema", tags=["Info Sistema"])
# controller = InfoSistemaController()


# @router.get(path="/", response_model=dict)
# async def obter_info_sistema() -> dict[str, str]:
#     """
#     Retorna o nome do sistema operacional e do usuário logado.
#     """
#     try:
#         resultado: InfoSistemaOut = controller.obter_info()
#         return dict(resultado.model_dump())
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(object=e)) from e
# """
# Rotas da API para ler o conteúdo de diretórios.
# """

# from fastapi import APIRouter, HTTPException, Query

# from core.controllers.explorador_controller import ExploradorController
# from core.models.modelos_api import ItemDePasta
# from core.models.models_exceptions import (
#     CaminhoNaoEncontradoError,
#     CaminhoNaoEDiretorioError,
#     PermissaoNegadaError,
# )

# router = APIRouter(prefix="/coletar_conteudo", tags=["Explorador"])
# controller = ExploradorController()


# @router.get(path="/", response_model=list[ItemDePasta])
# async def ler_e_listar_pasta(
#     caminho: str = Query(default=..., description="Caminho do diretório a ser listado"),
# ) -> list[ItemDePasta]:
#     """
#     Retorna a lista de arquivos e pastas presentes no diretório especificado.

#     Parâmetros:
#         caminho (str): Caminho absoluto do diretório.

#     Retorna:
#         list[ItemDePasta]: Lista contendo nome e tipo de cada item.

#     Erros:
#         404: Caminho não encontrado.
#         400: Caminho não é um diretório.
#         403: Permissão negada.
#         500: Erro interno inesperado.
#     """
#     try:
#         return controller.listar_itens_da_pasta(caminho=caminho)
#     except CaminhoNaoEncontradoError as e:
#         raise HTTPException(status_code=404, detail=str(e)) from e
#     except CaminhoNaoEDiretorioError as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e
#     except PermissaoNegadaError as e:
#         raise HTTPException(status_code=403, detail=str(e)) from e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}") from e


# router = APIRouter()


# # --- CONTEXTO: PASTA ---
# @router.get("/coletar_pastas", tags=["Pasta"])
# def listar_pastas(caminho: str) -> Pasta:
#     controller = PastaController()
#     return controller.carregar_pasta(caminho)


# # --- CONTEXTO: PROCESSADOR ---
# @router.get("/coletar_arquivos", tags=["Arquivos"])
# def listar_arquivos_em_pasta(caminho: str) -> list[str]:
#     return listar_arquivos_html(caminho)


# @router.get("/detalhes-arquivo", tags=["Arquivos"])
# def obter_detalhes_arquivo(caminho: str) -> dict:

#     return detalhar_arquivo(caminho)


# # --- CONTEXTO: VISOR ---
# @router.get("/conteudo-arquivo", tags=["Visualização"])
# def obter_conteudo_arquivo(caminho: str) -> list[str]:
#     return ler_conteudo_arquivo(caminho)


# # --- CONTEXTO: CONVERSÃO ---
# @router.post("/html-to-json", tags=["Conversão"])
# async def converter_html_para_json(file: UploadFile = File(...)) -> JSONResponse:
#     try:
#         conteudo = await file.read()
#         controller = ConversaoController()
#         resultado = controller.converter_html_para_json(conteudo)
#         return JSONResponse(content=resultado)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e


# @router.post("/converter-caminho-html", tags=["Conversão"])
# def converter_html_em_disco(caminho: str) -> JSONResponse:
#     try:
#         controller = ConversaoController()
#         resultado = controller.converter_arquivo_em_disco(caminho)
#         return JSONResponse(content=resultado)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e


# # --- CONTEXTO: SISTEMA ---
# @router.get("/infos-sistema", tags=["Sistema"])
# def infos_sistema() -> dict[str, str]:
#     return obter_infos_sistema()
