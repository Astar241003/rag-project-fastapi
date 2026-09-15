from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter(prefix="/register", tags=["register"])

@router.get("",include_in_schema=False)
async def router_register(request:Request):
    return templates.TemplateResponse(name="register.html",request=request)