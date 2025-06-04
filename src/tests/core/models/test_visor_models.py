# pylint: disable=import-error

"""
Testes para os modelos do visor do HTMLReader.

Este módulo testa a validação de caminhos, filtros, itens de pasta,
listas de itens e prévias de arquivos.
"""
from pathlib import Path

import pytest

from htmlreader.core.models.visor_models import CaminhoEntrada, FiltroVisor, ItemDePasta, ListaDeItens, PreviaArquivo


def test_caminho_entrada_valido(tmp_path: Path) -> None:
    """
    Testa se CaminhoEntrada aceita um caminho existente.
    """
    file = tmp_path / "arq.txt"
    file.write_text("abc")
    model = CaminhoEntrada(path=file)
    assert model.path == file


def test_caminho_entrada_invalido(tmp_path: Path) -> None:
    """
    Testa se CaminhoEntrada lança ValueError para caminho inexistente.
    """
    fake = tmp_path / "nao_existe.txt"
    with pytest.raises(ValueError):
        CaminhoEntrada(path=fake)


def test_filtro_visor() -> None:
    """
    Testa a criação do filtro do visor.
    """
    filtro = FiltroVisor(extensoes=[".txt", ".md"], tipo="arquivo")
    assert filtro.extensoes == [".txt", ".md"]
    assert filtro.tipo == "arquivo"


def test_item_de_pasta(tmp_path: Path) -> None:
    """
    Testa a criação de um ItemDePasta.
    """
    file = tmp_path / "arq.txt"
    file.write_text("abc")
    item = ItemDePasta(nome="arq.txt", path=file, tipo="arquivo")
    assert item.nome == "arq.txt"
    assert item.tipo == "arquivo"


def test_lista_de_itens(tmp_path: Path) -> None:
    """
    Testa a criação e o método __len__ de ListaDeItens.
    """
    file = tmp_path / "a.txt"
    file.write_text("abc")
    item = ItemDePasta(nome="a.txt", path=file, tipo="arquivo")
    lista = ListaDeItens(itens=[item])
    assert len(lista) == 1


def test_previa_arquivo() -> None:
    """
    Testa a criação de uma PreviaArquivo.
    """
    previa = PreviaArquivo(
        nome="arq.txt",
        extensao=".txt",
        tamanho_bytes=10,
        modificado_em="2024-01-01 10:00:00",
        linhas=["linha1", "linha2"],
    )
    assert previa.nome == "arq.txt"
    assert previa.extensao == ".txt"
    assert previa.linhas == ["linha1", "linha2"]
