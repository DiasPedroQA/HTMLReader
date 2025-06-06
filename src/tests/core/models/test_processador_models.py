"""
Testes unitários para os modelos definidos em htmlreader.core.models.objects_models.

Este módulo testa:
- Validação de caminhos de arquivos e pastas com Pydantic.
- Modelos de resultado de processamento.
- Lotes de arquivos para entrada em massa.
- Modelos relacionados à visualização (itens de pasta, filtros, prévias).
- Exceções customizadas que representam falhas específicas do domínio do HTMLReader.
"""

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
import pytest

from htmlreader.core.models.objects_models import (
    CaminhoArquivo,
    ResultadoProcessamento,
    LoteDeArquivos,
    CaminhoEntrada,
    FiltroVisor,
    ItemDePasta,
    ListaDeItens,
    PreviaArquivo,
    CaminhoInvalidoError,
    ArquivoNaoSuportadoError,
    ErroDeProcessamento,
)


# --- Testes para CaminhoArquivo ---


def test_caminho_arquivo_valido():
    """
    Testa se o modelo CaminhoArquivo aceita um caminho de arquivo existente.
    """
    with NamedTemporaryFile(delete=True) as tmp:
        caminho = Path(tmp.name)
        modelo = CaminhoArquivo(caminho_arquivo=caminho)
        assert modelo.caminho_arquivo == caminho


def test_caminho_arquivo_invalido():
    """
    Testa se CaminhoArquivo lança ValueError ao receber um caminho inexistente.
    """
    with pytest.raises(ValueError, match="Arquivo não existe"):
        CaminhoArquivo(caminho_arquivo=Path("/caminho/que/nao/existe.txt"))


# --- Testes para ResultadoProcessamento ---


def test_resultado_processamento_sucesso():
    """
    Testa a construção do modelo ResultadoProcessamento em caso de sucesso.
    """
    resultado = ResultadoProcessamento(
        caminho_entrada_arquivo=Path("/tmp/entrada.html"),
        caminho_saida_arquivo=Path("/tmp/saida.json"),
        processamento_bem_sucedido=True,
        mensagem_resultado="Processado com sucesso",
    )
    assert resultado.processamento_bem_sucedido is True
    assert "entrada.html" in str(resultado)


# --- Testes para LoteDeArquivos ---


def test_lote_de_arquivos():
    """
    Testa o modelo LoteDeArquivos com múltiplos arquivos válidos.
    """
    with NamedTemporaryFile() as f1, NamedTemporaryFile() as f2:
        arq1 = CaminhoArquivo(caminho_arquivo=Path(f1.name))
        arq2 = CaminhoArquivo(caminho_arquivo=Path(f2.name))
        lote = LoteDeArquivos(lista_arquivos=[arq1, arq2])
        assert len(lote) == 2


# --- Testes para CaminhoEntrada ---


def test_caminho_entrada_valido():
    """
    Testa se CaminhoEntrada aceita uma pasta existente.
    """
    with TemporaryDirectory() as tmp:
        entrada = CaminhoEntrada(caminho_entrada=Path(tmp))
        assert entrada.caminho_entrada.exists()


def test_caminho_entrada_invalido():
    """
    Testa se CaminhoEntrada lança ValueError para um caminho inexistente.
    """
    with pytest.raises(ValueError):
        CaminhoEntrada(caminho_entrada=Path("/nao/existe"))


# --- Testes para FiltroVisor ---


def test_filtro_visor_basico():
    """
    Testa criação de FiltroVisor com lista de extensões e tipo de item.
    """
    filtro = FiltroVisor(lista_extensoes=[".html", ".xml"], tipo_item="arquivo")
    assert ".html" in list(filtro.lista_extensoes)
    assert filtro.tipo_item == "arquivo"


# --- Testes para ItemDePasta e ListaDeItens ---


def test_item_de_pasta():
    """
    Testa representação de um item de pasta como arquivo.
    """
    caminho = Path("/tmp/exemplo.txt")
    item = ItemDePasta(
        nome_item="exemplo.txt", caminho_pasta_item=caminho, tipo_item="arquivo"
    )
    assert item.tipo_item == "arquivo"
    assert "exemplo.txt" in str(item)


def test_lista_de_itens():
    """
    Testa o modelo ListaDeItens com múltiplos itens (arquivo e pasta).
    """
    item1 = ItemDePasta(
        nome_item="a.txt", caminho_pasta_item=Path("/tmp/a.txt"), tipo_item="arquivo"
    )
    item2 = ItemDePasta(
        nome_item="b", caminho_pasta_item=Path("/tmp/b"), tipo_item="pasta"
    )
    lista = ListaDeItens(lista_itens=[item1, item2])
    assert len(lista) == 2


# --- Testes para PreviaArquivo ---


def test_previa_arquivo_repr():
    """
    Testa se o modelo PreviaArquivo apresenta corretamente o número de linhas.
    """
    previa = PreviaArquivo(
        nome_arquivo="teste.html",
        extensao_arquivo=".html",
        tamanho_em_bytes=1024,
        data_modificacao="2024-01-01 12:00",
        linhas_arquivo=["<html>", "<body>", "</body>", "</html>"],
    )
    assert "4 linhas" in str(previa)
    assert previa.extensao_arquivo == ".html"


# --- Testes para exceções customizadas ---


def test_caminho_invalido_error():
    """
    Testa se CaminhoInvalidoError é lançado com mensagem personalizada.
    """
    with pytest.raises(CaminhoInvalidoError) as exc:
        raise CaminhoInvalidoError("Caminho quebrado")
    assert "Caminho quebrado" in str(exc.value)


def test_arquivo_nao_suportado_error():
    """
    Testa se ArquivoNaoSuportadoError é lançado com a mensagem padrão.
    """
    with pytest.raises(ArquivoNaoSuportadoError):
        raise ArquivoNaoSuportadoError()


def test_erro_de_processamento():
    """
    Testa se ErroDeProcessamento é lançado com mensagem personalizada.
    """
    with pytest.raises(ErroDeProcessamento) as exc:
        raise ErroDeProcessamento("Erro no parser")
    assert "Erro no parser" in str(exc.value)
