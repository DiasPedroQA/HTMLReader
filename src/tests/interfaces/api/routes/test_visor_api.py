# """
# Módulo de testes para os endpoints da API do visor.

# Este módulo contém testes para os endpoints relacionados à listagem de conteúdo,
# verificando se o endpoint /listar retorna corretamente uma lista de itens filtrados
# por extensão de arquivo.

# Funções:
#     test_listar_conteudo: Testa o endpoint /listar para garantir que retorna uma lista de itens
#     ao receber um payload com caminho de diretório e filtros de extensão.
# """

# import pytest
# from fastapi.testclient import TestClient
# from htmlreader.interfaces.api.routes.visor_routes import router

# client = TestClient(router)


# @pytest.mark.asyncio
# async def test_listar_conteudo():
#     """
#     Testa o endpoint /listar da API.

#     Envia um payload contendo o caminho de um diretório e filtros de extensão de arquivo,
#     e verifica se a resposta possui status 200 e se o corpo da resposta é uma lista,
#     conforme esperado para o retorno de ListaDeItens.
#     """
#     # Teste para o endpoint /listar
#     payload = {
#         "path": "/caminho/do/diretorio",
#         "filtros": {"extensoes": [".html"]},
#     }
#     response = client.post("/listar", json=payload)
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)  # Supondo que ListaDeItens seja uma lista


# @pytest.mark.asyncio
# async def test_obter_previa():
#     """
#     Testa o endpoint /previa da API.

#     Este teste envia uma requisição POST para o endpoint /previa com um
#     payload contendo o caminho de um arquivo.
#     Verifica se a resposta possui status 200 e se o campo "conteudo"
#     está presente no JSON de resposta.

#     Pré-condições:
#     - O cliente da API (`client`) deve estar configurado.
#     - O arquivo especificado no payload deve existir e ser acessível pelo endpoint.

#     Asserções:
#     - O status da resposta deve ser 200 (OK).
#     - O JSON de resposta deve conter a chave "conteudo".
#     """
#     # Teste para o endpoint /previa
#     payload = {"path": "/caminho/do/arquivo.txt"}
#     response = client.post("/previa", json=payload)
#     assert response.status_code == 200
#     assert "conteudo" in response.json()
