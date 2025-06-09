from pydantic import BaseModel
from core.models.objects_models import Arquivo


class Pasta(BaseModel):
    nome: str
    caminho: str
    arquivos: list[Arquivo] = []
    subpastas: list["Pasta"] = []

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


Pasta.update_forward_refs()
