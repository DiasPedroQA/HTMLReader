import json
from bs4 import BeautifulSoup, Tag


def converter_html_para_json(conteudo_arquivo: str) -> str:
    soup_html = BeautifulSoup(conteudo_arquivo, "html.parser")
    dados = []

    for link_tag in soup_html.find_all("a"):
        if isinstance(link_tag, Tag):
            props = {
                k.lower(): v for k, v in link_tag.attrs.items()
            }  # todas as propriedades
            props["texto"] = link_tag.get_text(strip=True)
            dados.append(props)

    return json.dumps({"links": dados}, ensure_ascii=False, indent=2)


# html = """
# <DT><A HREF="https://morioh.com/p/2abbd072e6f6" ADD_DATE="1581896621" LAST_MODIFIED="1726334300">
# Como converter fala em texto em Python
# </A>
# """

# soup = BeautifulSoup(html, "html.parser")
# tag = soup.find("a")

# if isinstance(tag, Tag):
#     propriedades = {k.lower(): v for k, v in tag.attrs.items()}
#     propriedades["texto"] = tag.get_text(strip=True)

# print(propriedades)
