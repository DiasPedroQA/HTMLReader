"""
Testes para os modelos de processamento do HTMLReader.

Este módulo testa a validação de caminhos,
o funcionamento dos modelos de resultado e lote,
e as exceções customizadas do processador.
"""

from pathlib import Path
import pytest
from htmlreader.core.models.processador_models import (
    CaminhoArquivo,
    ResultadoProcessamento,
    LoteDeArquivos,
    CaminhoInvalidoError,
    ArquivoNaoSuportadoError,
    ErroDeProcessamento,
)


def test_caminho_arquivo_valido(tmp_path: Path) -> None:
    """
    Testa se CaminhoArquivo aceita um arquivo existente.
    """
    file = tmp_path / "arq.txt"
    file.write_text("abc")
    model = CaminhoArquivo(path=file)
    assert model.path == file


def test_caminho_arquivo_invalido(tmp_path: Path) -> None:
    """
    Testa se CaminhoArquivo lança ValueError para arquivo inexistente.
    """
    fake = tmp_path / "nao_existe.txt"
    with pytest.raises(ValueError):
        CaminhoArquivo(path=fake)


def test_resultado_processamento_str(tmp_path: Path) -> None:
    """
    Testa a representação em string do ResultadoProcessamento.
    """
    entrada = tmp_path / "in.txt"
    saida = tmp_path / "out.txt"
    res = ResultadoProcessamento(
        entrada=entrada, saida=saida, sucesso=True, mensagem="OK"
    )
    assert "Sucesso" in str(res)
    res2 = ResultadoProcessamento(
        entrada=entrada, saida=saida, sucesso=False, mensagem="Falha"
    )
    assert "Falha" in str(res2)


def test_lote_de_arquivos_len(tmp_path: Path) -> None:
    """
    Testa o método __len__ de LoteDeArquivos.
    """
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("1")
    file2.write_text("2")
    lote = LoteDeArquivos(
        arquivos=[CaminhoArquivo(path=file1), CaminhoArquivo(path=file2)]
    )
    assert len(lote) == 2


def test_excecoes_customizadas():
    """
    Testa se as exceções customizadas podem ser lançadas e capturadas.
    """
    with pytest.raises(CaminhoInvalidoError):
        raise CaminhoInvalidoError()
    with pytest.raises(ArquivoNaoSuportadoError):
        raise ArquivoNaoSuportadoError("Arquivo não suportado customizado.")
    with pytest.raises(ErroDeProcessamento):
        raise ErroDeProcessamento("Erro customizado.")
