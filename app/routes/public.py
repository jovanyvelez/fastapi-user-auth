"""Rutas públicas (autenticación)"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ..auth import get_optional_user
from ..config import templates
from ..database import get_db
from ..models import User
from ..services import AuthService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request, user: Annotated[Optional[User], Depends(get_optional_user)]
):
    """Página de inicio"""
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: Optional[str] = None):
    """Formulario de login"""
    if next:
        request.session["redirect_after_login"] = next

    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
async def login(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...),
):
    """Procesa login con validación"""

    user = AuthService.authenticate_user(db, username, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuario o contraseña incorrectos"},
            status_code=401,
        )

    # Guardar como dict en sesión (Pydantic → dict)
    request.session["user"] = user.model_dump()

    # Redirect after login
    redirect_url = request.session.pop("redirect_after_login", "/dashboard")
    if not redirect_url.startswith("/"):
        redirect_url = "/dashboard"

    return RedirectResponse(url=redirect_url, status_code=303)


@router.get("/logout")
async def logout(request: Request):
    """Cerrar sesión"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
