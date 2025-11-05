"""Aplicación principal FastAPI"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.config import SECRET_KEY, templates
from app.routes import admin, protected, public

# ==================== INICIALIZACIÓN ====================

app = FastAPI(
    title="FastAPI User Auth",
    description="Sistema de autenticación con roles y permisos",
    version="1.0.0",
)

# Middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Registro de routers
app.include_router(public.router, tags=["Public"])
app.include_router(protected.router, tags=["Protected"])
app.include_router(admin.router, tags=["Admin"])


# ==================== MANEJO DE ERRORES ====================


@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: HTTPException):
    """Redirige al login si no está autenticado"""
    return RedirectResponse(url="/login", status_code=303)


@app.exception_handler(403)
async def forbidden_handler(request: Request, exc: HTTPException):
    """Maneja errores de permisos insuficientes"""
    return templates.TemplateResponse(
        "error_403.html", {"request": request, "message": exc.detail}, status_code=403
    )
