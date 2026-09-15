from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import HTMLResponse
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("", include_in_schema=False)
async def router_chat(request:Request):
    return templates.TemplateResponse(name="chat.html",request=request)