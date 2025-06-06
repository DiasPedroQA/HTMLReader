# """
# Serviços de processamento de arquivos para o HTMLReader.

Inclui funções para processar arquivos individuais e em lote,
gerando arquivos de saída com novo conteúdo e lidando com erros de processamento.
"""

from pathlib import Path

from htmlreader.core.models.processador_models import (
    ErroDeProcessamento,
    LoteDeArquivos,
    ResultadoProcessamento,
)


def processar_arquivo(
    caminho: Path, tipo_saida: str = ".json"
) -> ResultadoProcessamento:
    """
    Processa um arquivo, gerando um novo arquivo de saída com o conteúdo convertido.

    Args:
        caminho (Path): Caminho do arquivo de entrada.
        tipo_saida (str, opcional): Extensão do arquivo de saída (default: ".json").

    Returns:
        ResultadoProcessamento: Resultado do processamento, incluindo caminhos e status.

    Raises:
        ErroDeProcessamento: Se ocorrer qualquer erro durante o processamento.
    """
    try:
        conteudo = caminho.read_text(encoding="utf-8")
        novo_caminho = caminho.with_suffix(tipo_saida)
        novo_caminho.write_text(f"# Convertido\n\n{conteudo}", encoding="utf-8")
        return ResultadoProcessamento(
            entrada=caminho, saida=novo_caminho, sucesso=True, mensagem="OK"
        )
    except Exception as e:
        raise ErroDeProcessamento(str(e)) from e


def processar_em_lote(
    lote: LoteDeArquivos, tipo_saida: str = ".json"
) -> list[ResultadoProcessamento]:
    """
    Processa um lote de arquivos, retornando os resultados individuais de cada arquivo.

    Args:
        lote (LoteDeArquivos): Lote contendo os arquivos a serem processados.
        tipo_saida (str, opcional): Extensão dos arquivos de saída (default: ".json").

    Returns:
        list[ResultadoProcessamento]: Lista de resultados do processamento
        de cada arquivo.
    """
    resultados = []
    for item in lote.arquivos:
        try:
            resultado = processar_arquivo(item.path, tipo_saida)
        except ErroDeProcessamento as e:
            resultado = ResultadoProcessamento(
                entrada=item.path, saida=Path(""), sucesso=False, mensagem=str(e)
            )
        resultados.append(resultado)
    return resultados
