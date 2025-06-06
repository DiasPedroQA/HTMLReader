# """
# Testes para o módulo processador_service do HTMLReader.
# """

# from pathlib import Path
# import pytest
# from htmlreader.core.services import processar_arquivo, processar_em_lote
# from htmlreader.core.models.processador_models import (
#     LoteDeArquivos,
#     ResultadoProcessamento,
#     ErroDeProcessamento,
#     CaminhoArquivo,
# )


# def test_processar_arquivo_sucesso(tmp_path: Path) -> None:
#     """
#     Testa o processamento de um arquivo válido.
#     """
#     file = tmp_path / "arq.txt"
#     file.write_text("conteudo")
#     resultado = processar_arquivo(file)
#     assert isinstance(resultado, ResultadoProcessamento)
#     assert resultado.sucesso is True
#     assert resultado.saida.exists()
#     assert resultado.saida.read_text(encoding="utf-8").startswith("# Convertido")


# def test_processar_arquivo_erro(tmp_path: Path) -> None:
#     """
#     Testa o processamento de um arquivo inexistente (deve lançar ErroDeProcessamento).
#     """
#     fake = tmp_path / "nao_existe.txt"
#     with pytest.raises(ErroDeProcessamento):
#         processar_arquivo(fake)


# def test_processar_em_lote(tmp_path: Path) -> None:
#     """
#     Testa o processamento em lote de arquivos.
#     """
#     file1 = tmp_path / "a.txt"
#     file2 = tmp_path / "b.txt"
#     file1.write_text("abc")
#     file2.write_text("def")
#     lote = LoteDeArquivos(
#         arquivos=[CaminhoArquivo(path=file1), CaminhoArquivo(path=file2)]
#     )
#     resultados = processar_em_lote(lote)
#     assert len(resultados) == 2
#     assert all(isinstance(r, ResultadoProcessamento) for r in resultados)
#     assert all(r.sucesso for r in resultados)


# def test_processar_em_lote_com_erro(tmp_path: Path) -> None:
#     """
#     Testa o processamento em lote com um arquivo inexistente.
#     """
#     file1 = tmp_path / "a.txt"
#     file1.write_text("abc")
#     fake = tmp_path / "nao_existe.txt"
#     lote = LoteDeArquivos(
#         arquivos=[CaminhoArquivo(path=file1), CaminhoArquivo(path=fake)]
#     )
#     resultados = processar_em_lote(lote)
#     assert len(resultados) == 2
#     assert resultados[0].sucesso is True
#     assert resultados[1].sucesso is False
#     assert (
#         "não existe" in resultados[1].mensagem
#         or "No such file" in resultados[1].mensagem
#     )
