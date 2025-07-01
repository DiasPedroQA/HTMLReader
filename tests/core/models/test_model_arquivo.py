# """
# Testes unitários para o modelo `Arquivo`.

# Este módulo cobre:
# - Verificação de existência e metadados
# - Leitura e escrita de conteúdo
# - Detecção de arquivos ocultos
# - Comportamento de caminhos inválidos
# """

# from pathlib import Path
# from typing import NoReturn

# from pytest import MonkeyPatch

# from core.models.model_arquivo import Arquivo


# class TestArquivo:
#     """Classe de testes para o modelo `Arquivo`."""

#     def test_arquivo_valido(self, tmp_path: Path) -> None:
#         """Testa a criação, escrita e leitura de um arquivo válido."""
#         caminho: Path = tmp_path / "teste.txt"
#         arq = Arquivo(caminho=caminho)
#         conteudo = "exemplo de conteúdo"

#         assert arq.criar(conteudo=conteudo) is True
#         assert arq.existe is True
#         assert arq.nome == "teste.txt"
#         assert arq.extensao == "txt"
#         assert arq.ler() == conteudo
#         assert arq.tamanho_bytes > 0
#         assert arq.diretorio_pai == tmp_path
#         assert arq.eh_oculto is False

#     def test_arquivo_invalido(self, tmp_path: Path) -> None:
#         """Testa a leitura e propriedades de um arquivo inexistente."""
#         caminho: Path = tmp_path / "invalido.txt"
#         arq = Arquivo(caminho=caminho)

#         assert arq.existe is False
#         assert arq.ler() is None
#         assert arq.tamanho_bytes == 0
#         assert arq.criado_em is None
#         assert arq.modificado_em is None

#     def test_arquivo_oculto(self, tmp_path: Path) -> None:
#         """Testa a detecção de um arquivo oculto (nome iniciado por ponto)."""
#         caminho: Path = tmp_path / ".segredo"
#         caminho.write_text("conteúdo sigiloso")
#         arq = Arquivo(caminho=caminho)

#         assert arq.eh_oculto is True

#     def test_operadores_personalizados(self, tmp_path: Path) -> None:
#         """Testa operadores personalizados: /, str e repr."""
#         caminho: Path = tmp_path / "exemplo.txt"
#         caminho.write_text("abc")
#         arq = Arquivo(caminho=caminho)

#         sub_arq: Arquivo = arq / "outro.txt"
#         assert isinstance(sub_arq, Arquivo)
#         assert str(arq) == str(caminho)
#         assert repr(arq).startswith("Arquivo(")

#     def test_ler_erro_codificacao(self, tmp_path: Path) -> None:
#         """Testa erro de leitura com conteúdo binário inválido."""
#         caminho: Path = tmp_path / "binario.txt"
#         caminho.write_bytes(b"\xff\xfe")  # dados inválidos para UTF-8
#         arq = Arquivo(caminho=caminho)

#         assert arq.ler() is None

#     def test_tamanho_e_datas_de_arquivo_inexistente(self, tmp_path: Path) -> None:
#         """Testa métodos que dependem de stat em arquivos removidos."""
#         caminho: Path = tmp_path / "apagado.txt"
#         caminho.write_text("teste")
#         arq = Arquivo(caminho=caminho)
#         caminho.unlink()  # remove o arquivo

#         assert arq.tamanho_bytes == 0
#         assert arq.criado_em is None
#         assert arq.modificado_em is None

#     def test_criar_falha_por_oserror(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
#         """Testa falha de criação de arquivo simulando OSError."""

#         caminho: Path = tmp_path / "erro.txt"
#         arq = Arquivo(caminho=caminho)

#         def fake_write_text(*args, **kwargs) -> NoReturn:
#             raise OSError("Erro simulado")

#         monkeypatch.setattr(target=Path, name="write_text", value=fake_write_text)

#         assert arq.criar(conteudo="dados") is False
