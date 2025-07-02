# # pylint: disable=W0621

# """
# Testes automatizados para a classe ArquivosController,
# responsável pela manipulação de arquivos.
# """

# from pathlib import Path

# import pytest

# from src.core.controllers.arquivos_controller import ArquivosController
# from src.core.models.model_arquivo import Arquivo


# @pytest.fixture
# def arquivos_controller() -> ArquivosController:
#     """Instancia o controlador de arquivos a ser usado nos testes."""
#     return ArquivosController()


# class TestArquivosController:
#     """
#     Classe de testes para o controlador ArquivosController,
#     que gerencia arquivos do sistema.
#     """

#     def test_criar_arquivo_sem_conteudo(
#         self, tmp_path: Path, arquivos_controller: ArquivosController
#     ) -> None:
#         """Deve criar um arquivo vazio se nenhum conteúdo for fornecido."""
#         caminho: Path = tmp_path / "teste.txt"
#         assert not caminho.exists()
#         arquivo: Arquivo = arquivos_controller.criar_arquivo(caminho_arquivo=caminho)
#         assert caminho.exists()
#         assert arquivo.ler_conteudo() == ""

#     def test_criar_arquivo_com_conteudo(
#         self, tmp_path: Path, arquivos_controller: ArquivosController
#     ) -> None:
#         """Deve criar um arquivo com o conteúdo especificado."""
#         caminho: Path = tmp_path / "documento.txt"
#         conteudo = "Olá, mundo!"
#         arquivo: Arquivo = arquivos_controller.criar_arquivo(
#             caminho_arquivo=caminho, conteudo=conteudo
#         )
#         assert caminho.exists()
#         assert caminho.read_text(encoding="utf-8") == conteudo
#         assert arquivo.ler_conteudo() == conteudo

#     def test_ler_conteudo_arquivo_existente(
#         self, tmp_path: Path, arquivos_controller: ArquivosController
#     ) -> None:
#         """Deve retornar corretamente o conteúdo de um arquivo existente."""
#         caminho: Path = tmp_path / "lido.txt"
#         texto = "Conteúdo de teste."
#         caminho.write_text(data=texto, encoding="utf-8")
#         conteudo_lido: str | None = arquivos_controller.ler_conteudo_arquivo(
#             caminho_arquivo=caminho
#         )
#         assert conteudo_lido == texto

#     def test_ler_metadados_arquivo(
#         self, tmp_path: Path, arquivos_controller: ArquivosController
#     ) -> None:
#         """Deve retornar os metadados corretos de um arquivo."""
#         caminho: Path = tmp_path / "dados.log"
#         caminho.write_text(data="log de sistema", encoding="utf-8")
#         metadados: dict[str, str | None] = arquivos_controller.ler_metadados_arquivo(
#             caminho_arquivo=caminho
#         )
#         assert metadados["nome"] == "dados.log"
#         assert metadados["extensao_arquivo"] == ".log"
#         assert metadados["nome_sem_extensao"] == "dados"
#         assert metadados["extensao_legivel"] == "Log"
#         assert metadados["eh_oculto"] == "Não"
#         assert isinstance(metadados["tamanho_legivel"], str)
#         assert isinstance(metadados["data_criacao"], str)
#         assert isinstance(metadados["data_modificacao"], str)

#     def test_criar_arquivo_em_arquivo_oculto(
#         self, tmp_path: Path, arquivos_controller: ArquivosController
#     ) -> None:
#         """Deve lidar corretamente com arquivos ocultos (prefixo com ponto)."""
#         caminho: Path = tmp_path / ".oculto"
#         arquivo: Arquivo = arquivos_controller.criar_arquivo(
#             caminho_arquivo=caminho, conteudo="segredo"
#         )
#         assert arquivo.eh_arquivo_oculto is True
#         assert arquivo.nome_caminho == ".oculto"
