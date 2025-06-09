from __future__ import annotations

from pathlib import Path
import json
from typing import List, Optional

from bs4 import BeautifulSoup, Tag
from core.models.conversao_models import LinkExtraido, ResultadoConversao


class ConversorHTMLService:
    @staticmethod
    def extrair_links(html: str) -> List[LinkExtraido]:
        """
        Extrai todos os links <a> do conteúdo HTML e retorna uma lista de objetos LinkExtraido.

        Args:
            html (str): Conteúdo HTML a ser processado.

        Returns:
            List[LinkExtraido]: Lista de links extraídos do HTML.
        """

        def str_attr(value: Optional[str]) -> Optional[str]:
            """
            Normaliza o valor do atributo para str ou None.
            Retorna None se o valor for None ou string vazia.

            Args:
                value (Optional[str]): Valor do atributo HTML.

            Returns:
                Optional[str]: Valor normalizado ou None.
            """
            if value is None or value == "":
                return None
            return value

        soup = BeautifulSoup(html, "html.parser")
        elementos = soup.find_all("a")

        links: List[LinkExtraido] = []
        for el in elementos:
            if isinstance(el, Tag):
                href_value = el.get("href", "")
                href: str | None = str_attr(
                    href_value
                    if isinstance(href_value, str) or href_value is None
                    else str(href_value)
                )
                add_date_value = el.get("ADD_DATE", "")
                add_date: str | None = str_attr(
                    add_date_value
                    if isinstance(add_date_value, str) or add_date_value is None
                    else str(add_date_value)
                )
                last_modified_value = el.get("LAST_MODIFIED", "")
                last_modified: str | None = str_attr(
                    last_modified_value
                    if isinstance(last_modified_value, str)
                    or last_modified_value is None
                    else str(last_modified_value)
                )

                # Considerando que href é obrigatório no LinkExtraido, substitui None por string vazia
                if href is None:
                    href = ""

                link = LinkExtraido(
                    texto=el.get_text(strip=True),
                    href=href,
                    add_date=add_date,
                    last_modified=last_modified,
                )
                links.append(link)

        return links

    @staticmethod
    def converter_arquivo_html(
        caminho_arquivo: str, caminho_saida: str
    ) -> ResultadoConversao:
        """
        Converte o conteúdo de um arquivo HTML em uma estrutura JSON de links extraídos.

        Args:
            caminho_arquivo (str): Caminho do arquivo HTML de origem.
            caminho_saida (str): Caminho do arquivo JSON de saída.

        Returns:
            ResultadoConversao: Objeto contendo informações sobre a conversão realizada.
        """
        caminho_origem = Path(caminho_arquivo)
        caminho_destino = Path(caminho_saida)

        with caminho_origem.open("r", encoding="utf-8") as f:
            conteudo = f.read()

        links = ConversorHTMLService.extrair_links(conteudo)

        resultado = ResultadoConversao(
            caminho_origem=str(caminho_origem),
            caminho_destino=str(caminho_destino),
            total_links=len(links),
            links=links,
        )

        with caminho_destino.open("w", encoding="utf-8") as f:
            json.dump(
                resultado.model_dump(by_alias=True),
                f,
                ensure_ascii=False,
                indent=4,
            )

        return resultado
