"""Servicios de lógica de negocio"""

from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import verify_password
from .models import User


class AuthService:
    """Servicio para manejar la autenticación de usuarios"""

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Autentica un usuario verificando sus credenciales.

        Args:
            db: Sesión de base de datos
            username: Nombre de usuario
            password: Contraseña en texto plano

        Returns:
            User si las credenciales son válidas, None en caso contrario
        """
        result = db.execute(
            text(
                "SELECT username, name, hashed_pass, email, role FROM users WHERE username = :username"
            ),
            {"username": username},
        ).fetchone()

        if not result:
            return None

        if not verify_password(password, result.hashed_pass):
            return None

        # Crear objeto User (sin password)
        return User(
            username=result.username,
            name=result.name,
            email=result.email,
            role=result.role,
        )
