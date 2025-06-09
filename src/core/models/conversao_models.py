from pydantic import BaseModel


class LinkExtraido(BaseModel):
    add_date: str | None = None
    last_modified: str | None = None
    href: str
    texto: str


class ResultadoConversao(BaseModel):
    caminho_origem: str
    caminho_destino: str
    total_links: int
    links: list[LinkExtraido]
