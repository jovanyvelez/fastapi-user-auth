from pydantic import BaseModel, Field


class User(BaseModel):
    """Modelo del usuario autenticado"""

    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    email: str | None = None
    role: str = "user"  # Útil para roles/permisos

    class Config:
        # Permite acceso con user.username en templates
        from_attributes = True


class UserInDB(BaseModel):
    """Modelo para datos almacenados en BD (incluye hashed_pass)"""

    username: str
    name: str
    hashed_pass: str  # Hasheado con argon2
    email: str | None = None
    role: str = "user"
