# routes.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..settings import get_settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    settings = get_settings()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "mapbox_access_token": settings.mapbox_access_token.get_secret_value(),
        },
    )
