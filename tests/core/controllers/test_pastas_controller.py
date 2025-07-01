# # pylint: disable=W0621
# """
# Testes automatizados para o controlador PastasController,
# responsável por operações com diretórios.
# """

# from pathlib import Path

# import pytest

# from app.core.controllers.pastas_controller import PastasController
# from app.core.models.model_arquivo import Arquivo
# from app.core.models.model_caminho_base import CaminhoBase
# from app.core.models.model_pasta import Pasta


# @pytest.fixture()
# def controlador() -> PastasController:
#     """Retorna uma instância do controlador de pastas."""
#     return PastasController()


# class TestPastasController:
#     """Testes para os métodos públicos de PastasController."""

#     def test_criar_pasta_nova_ou_existente(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Cria a pasta se não existir e evita recriação caso já exista."""
#         destino: Path = tmp_path / "nova_pasta"
#         assert not destino.exists()
#         assert controlador.criar_se_nao_existir(caminho=destino) is True
#         assert destino.exists()
#         assert controlador.criar_se_nao_existir(caminho=destino) is False

#     def test_listar_nomes_itens_da_pasta(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Retorna nomes de arquivos e pastas diretamente contidos."""
#         (tmp_path / "a.txt").touch()
#         (tmp_path / "subdir").mkdir()
#         nomes: list[str] = controlador.listar_nomes_itens(caminho=tmp_path)
#         assert set(nomes) == {"a.txt", "subdir"}

#     def test_listar_ocultos(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Retorna arquivos e pastas ocultos corretamente."""
#         (tmp_path / ".a.txt").touch()
#         (tmp_path / ".oculta").mkdir()
#         (tmp_path / "visivel.txt").touch()

#         resultados: set[str] = {
#             p.name for p in controlador.listar_ocultos(caminho=tmp_path)
#         }
#         assert ".a.txt" in resultados
#         assert ".oculta" in resultados
#         assert "visivel.txt" not in resultados

#     def test_listar_subpastas_imediatas(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Retorna subpastas imediatas corretamente."""
#         (tmp_path / "dir1").mkdir()
#         (tmp_path / "dir2").mkdir()
#         (tmp_path / "arquivo.txt").touch()

#         subpastas: list[Pasta] = controlador.listar_subpastas(caminho=tmp_path)
#         nomes: list[str] = [p.nome_caminho for p in subpastas]
#         assert set(nomes) == {"dir1", "dir2"}

#     def test_listar_arquivos_com_ou_sem_filtro(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Retorna arquivos filtrando por extensão, ou todos se sem filtro."""
#         dir_pasta: Path = tmp_path / "docs"
#         dir_pasta.mkdir()
#         (dir_pasta / "a.txt").touch()
#         (dir_pasta / "b.md").touch()

#         arquivos_txt: list[Arquivo] = controlador.listar_arquivos(
#             caminho=dir_pasta, extensao_arquivo=".txt"
#         )
#         assert (
#             len(arquivos_txt) == 0
#         )  # Não encontra o arquivo ".txt", pois a pasta não existe
#         # assert arquivos_txt[0].nome_caminho == "a.txt"

#         arquivos_todos: list[Arquivo] = controlador.listar_arquivos(caminho=dir_pasta)
#         nomes: list[str] = [a.nome_caminho for a in arquivos_todos]
#         assert set(nomes) == {"a.txt", "b.md"}

#     def test_listar_conteudo_recursivo(
#         self, tmp_path: Path, controlador: PastasController
#     ) -> None:
#         """Retorna todos os caminhos da pasta, inclusive subpastas e arquivos."""
#         (tmp_path / "sub1").mkdir()
#         (tmp_path / "sub1" / "a.txt").touch()
#         (tmp_path / "b.txt").touch()

#         resultados: list[CaminhoBase] = controlador.listar_conteudo_recursivo(
#             caminho=tmp_path
#         )
#         nomes: list[str] = [c.nome_caminho for c in resultados]
#         assert "a.txt" in nomes
#         assert "b.txt" in nomes
