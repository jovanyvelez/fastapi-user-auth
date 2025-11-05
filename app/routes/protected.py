"""Rutas protegidas (requieren autenticación)"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ..auth import get_current_user
from ..config import templates
from ..models import User

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: Annotated[User, Depends(get_current_user)],
):
    """Dashboard - Solo usuarios autenticados"""
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: Annotated[User, Depends(get_current_user)]):
    """Perfil del usuario"""
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )


@router.get("/dashboard/reportes", response_class=HTMLResponse)
async def reportes(request: Request, user: Annotated[User, Depends(get_current_user)]):
    """Reportes - Cualquier usuario autenticado"""
    return templates.TemplateResponse(
        "reportes.html", {"request": request, "user": user}
    )


@router.get("/configuracion", response_class=HTMLResponse)
async def configuracion(
    request: Request, user: Annotated[User, Depends(get_current_user)]
):
    """Configuración del sistema"""
    return templates.TemplateResponse(
        "configuracion.html", {"request": request, "user": user}
    )
