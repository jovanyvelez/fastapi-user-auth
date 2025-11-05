from typing import Annotated

from fastapi import Depends, HTTPException, Request

from .models import User


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


def get_optional_user(request: Request) -> User | None:
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
