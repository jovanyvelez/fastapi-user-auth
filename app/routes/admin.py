"""Rutas de administración (solo para admins)"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ..auth import require_admin
from ..config import templates
from ..models import User

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    admin: Annotated[User, Depends(require_admin)],
):
    """Panel de administración - SOLO ADMINS"""
    return templates.TemplateResponse("admin.html", {"request": request, "user": admin})
