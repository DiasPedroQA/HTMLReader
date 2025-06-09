from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from core.controllers.conversao_controller import ConversaoController

conversao_router = APIRouter()


@conversao_router.post("/html-to-json")
async def converter_html_para_json(file: UploadFile = File(...)) -> JSONResponse:
    try:
        conteudo = await file.read()
        controller = ConversaoController()
        resultado = controller.converter_html_para_json(conteudo)
        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
