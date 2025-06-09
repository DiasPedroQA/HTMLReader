from fastapi import APIRouter
from core.controllers.pasta_controller import PastaController
from core.models.pasta_models import Pasta

pasta_router = APIRouter()


@pasta_router.get("/listar-pastas")
def listar_pastas(caminho: str) -> Pasta:
    """
    Lista o conteúdo de uma pasta.
    """
    controller = PastaController()
    return controller.carregar_pasta(caminho)
