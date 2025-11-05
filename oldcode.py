from typing import Annotated, Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from starlette.middleware.sessions import SessionMiddleware

# ==================== MODELOS PYDANTIC ====================


class User(BaseModel):
    """Modelo del usuario autenticado"""

    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = None
    role: str = "user"  # Útil para roles/permisos

    class Config:
        # Permite acceso con user.username en templates
        from_attributes = True


class UserInDB(BaseModel):
    """Modelo para datos almacenados en BD (incluye hashed_pass)"""

    username: str
    name: str
    hashed_pass: str  # Hasheado con argon2
    email: Optional[str] = None
    role: str = "user"


# ==================== CONFIGURACIÓN SQLALCHEMY ====================

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


engine = create_engine(
    "sqlite:///users.db", echo=False, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ==================== INICIALIZACIÓN ====================

app = FastAPI()

SECRET_KEY = "d1e15362db01ebee6e3993ad6ddd0352acb4c46c1cc415de4c208922922764b2"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="templates")


# ==================== DEPENDENCIAS CON TIPADO ====================


def get_current_user(request: Request) -> User:
    """
    Verifica sesión y devuelve un objeto User tipado.
    Si no hay sesión, guarda la URL y lanza 401.
    """
    user_data = request.session.get("user")

    if not user_data:
        # Guardar URL original para redirect after login
        request.session["redirect_after_login"] = str(request.url.path)
        raise HTTPException(status_code=401, detail="No autenticado")

    # 🔥 Convertir dict a objeto User con validación
    try:
        return User(**user_data)
    except Exception:
        # Si los datos de sesión están corruptos, cerrar sesión
        request.session.clear()
        raise HTTPException(status_code=401, detail="Sesión inválida")


def get_optional_user(request: Request) -> Optional[User]:
    """Devuelve User si existe, None si no hay sesión"""
    user_data = request.session.get("user")
    if not user_data:
        return None

    try:
        return User(**user_data)
    except Exception:
        return None


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Dependencia adicional: requiere que el usuario sea admin.
    Se encadena con get_current_user.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: se requieren permisos de administrador",
        )
    return user


# ==================== RUTAS PÚBLICAS ====================


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request, user: Annotated[Optional[User], Depends(get_optional_user)]
):
    """Página de inicio"""
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: Optional[str] = None):
    """Formulario de login"""
    if next:
        request.session["redirect_after_login"] = next

    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
):
    """Procesa login con validación Pydantic"""

    # Buscar usuario en BD con SQL puro
    result = db.execute(
        text(
            "SELECT username, name, hashed_pass, email, role FROM users WHERE username = :username"
        ),
        {"username": username},
    ).fetchone()

    if not result or not verify_password(password, result.hashed_pass):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuario o contraseña incorrectos"},
            status_code=401,
        )

    # 🔥 Crear objeto User (sin password) y guardarlo en sesión
    user = User(
        username=result.username,
        name=result.name,
        email=result.email,
        role=result.role,
    )

    # Guardar como dict en sesión (Pydantic → dict)
    request.session["user"] = user.model_dump()

    # Redirect after login
    redirect_url = request.session.pop("redirect_after_login", "/dashboard")
    if not redirect_url.startswith("/"):
        redirect_url = "/dashboard"

    return RedirectResponse(url=redirect_url, status_code=303)


@app.get("/logout")
async def logout(request: Request):
    """Cerrar sesión"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


# ==================== RUTAS PROTEGIDAS ====================


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: Annotated[User, Depends(get_current_user)],  # 🔥 Tipado con Annotated
):
    """
    Dashboard - Solo usuarios autenticados.
    Ahora 'user' es un objeto User con tipado completo.
    """
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: Annotated[User, Depends(get_current_user)]):
    """Perfil del usuario"""
    # Ahora puedes usar: user.username, user.name, user.email con autocompletado
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )


@app.get("/dashboard/reportes", response_class=HTMLResponse)
async def reportes(request: Request, user: Annotated[User, Depends(get_current_user)]):
    """Reportes - Cualquier usuario autenticado"""
    return templates.TemplateResponse(
        "reportes.html", {"request": request, "user": user}
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    admin: Annotated[User, Depends(require_admin)],  # 🔥 Dependencia encadenada
):
    """
    Panel de administración - SOLO ADMINS.
    require_admin se encadena con get_current_user automáticamente.
    """
    return templates.TemplateResponse("admin.html", {"request": request, "user": admin})


@app.get("/configuracion", response_class=HTMLResponse)
async def configuracion(
    request: Request, user: Annotated[User, Depends(get_current_user)]
):
    """Configuración del sistema"""
    return templates.TemplateResponse(
        "configuracion.html", {"request": request, "user": user}
    )


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


# ==================== INSTRUCCIONES ====================
"""
MEJORAS CON PYDANTIC:
✅ Tipado fuerte con User model
✅ Validación automática de datos de sesión
✅ Autocompletado en IDE (user.username, user.name, etc.)
✅ Separación clara entre UserInDB (con password) y User (sin password)
✅ Dependencias encadenadas (require_admin depende de get_current_user)
✅ Conversión automática dict ↔ Pydantic

VENTAJAS DE Annotated:
- Sintaxis moderna y limpia
- Fácil de leer: Annotated[User, Depends(get_current_user)]
- Compatible con FastAPI 0.95+

EJEMPLO DE USO EN FUNCIÓN:
async def mi_ruta(user: Annotated[User, Depends(get_current_user)]):
    # Ahora tienes autocompletado:
    print(user.username)  # ✅
    print(user.name)      # ✅
    print(user.email)     # ✅
    print(user.role)      # ✅

DEPENDENCIAS ENCADENADAS:
require_admin → get_current_user → valida sesión y permisos automáticamente

USUARIOS DE PRUEBA:
- admin / admin123 (role: admin) → Puede acceder a /admin
- usuario / pass123 (role: user) → NO puede acceder a /admin

EJECUTAR:
uvicorn main:app --reload

BASE DE DATOS:
- SQLite con SQLAlchemy 2.0 (SQL puro con text())
- Contraseñas hasheadas con Argon2
- Tabla 'users' ya existente

PRUEBA:
1. Login como "usuario" → intenta ir a /admin → error 403
2. Login como "admin" → accede a /admin sin problemas ✅
"""
