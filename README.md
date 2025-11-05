# FastAPI User Authentication

Sistema de autenticación de usuarios con FastAPI, SQLite, SQLAlchemy y Argon2.

## 📁 Estructura del Proyecto

```
fastapi-user-auth/
├── main.py                 # Aplicación principal FastAPI
├── oldcode.py              # Código anterior (referencia)
├── app/                    # Paquete principal de la aplicación
│   ├── __init__.py
│   ├── config.py           # Configuración y constantes
│   ├── models.py           # Modelos Pydantic (User, UserInDB)
│   ├── database.py         # Configuración SQLAlchemy y funciones de hash
│   ├── auth.py             # Dependencias de autenticación
│   ├── services.py         # Lógica de negocio (AuthService)
│   └── routes/
│       ├── __init__.py
│       ├── public.py       # Rutas públicas (/, /login, /logout)
│       ├── protected.py    # Rutas protegidas (dashboard, profile, reportes, config)
│       └── admin.py        # Rutas de administración (solo admins)
├── templates/              # Templates HTML Jinja2
│   ├── home.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── reportes.html
│   ├── admin.html
│   ├── configuracion.html
│   └── error_403.html
├── users.db                # Base de datos SQLite
├── pyproject.toml          # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🔧 Arquitectura y Separación de Responsabilidades

### **`main.py`** - Punto de Entrada
- Inicializa la aplicación FastAPI
- Registra el middleware de sesiones
- Incluye los routers desde `app/` (public, protected, admin)
- Define manejadores globales de errores (401, 403)

```python
from app.config import SECRET_KEY, templates
from app.routes import admin, protected, public

app = FastAPI(title="FastAPI User Auth")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(public.router, tags=["Public"])
app.include_router(protected.router, tags=["Protected"])
app.include_router(admin.router, tags=["Admin"])
```

### **`app/config.py`** - Configuración
- Constantes globales (`SECRET_KEY`)
- Configuración de templates Jinja2
- Variables de entorno y configuración centralizada

### **`app/models.py`** - Modelos de Datos
- `User`: Modelo del usuario autenticado (sin contraseña)
- `UserInDB`: Modelo con `hashed_pass` para BD

### **`app/database.py`** - Capa de Datos
- Configuración del engine SQLAlchemy con SQLite
- `SessionLocal`: Generador de sesiones de BD
- `get_db()`: Dependencia para inyectar sesiones
- `hash_password()`: Hash de contraseñas con Argon2
- `verify_password()`: Verificación de contraseñas

### **`app/auth.py`** - Autenticación y Autorización
- `get_current_user()`: Valida sesión y retorna usuario
- `get_optional_user()`: Retorna usuario si existe sesión (opcional)
- `require_admin()`: Dependencia encadenada que valida rol admin

### **`app/services.py`** - Lógica de Negocio
- `AuthService.authenticate_user()`: Valida credenciales contra BD usando SQL puro
- Separa la lógica de autenticación de las rutas
- Retorna objeto `User` validado o `None`

### **`app/routes/`** - Routers Modulares

#### **`app/routes/public.py`**
- `GET /`: Página de inicio
- `GET /login`: Formulario de login
- `POST /login`: Procesa autenticación
- `GET /logout`: Cierra sesión

#### **`app/routes/protected.py`**
Rutas que requieren autenticación (`Depends(get_current_user)`):
- `GET /dashboard`: Panel principal
- `GET /profile`: Perfil del usuario
- `GET /dashboard/reportes`: Reportes
- `GET /configuracion`: Configuración

#### **`app/routes/admin.py`**
Rutas exclusivas para administradores (`Depends(require_admin)`):
- `GET /admin`: Panel de administración

## 🔄 Flujo de Autenticación

```
1. Usuario ingresa credenciales → POST /login
2. AuthService.authenticate_user() consulta BD con SQL puro
3. Verifica hash de contraseña con Argon2
4. Crea objeto User (sin password) y lo guarda en sesión
5. Redirecciona a /dashboard

En rutas protegidas:
1. get_current_user() lee sesión
2. Valida y convierte dict → User (Pydantic)
3. Si no hay sesión → 401 → redirect /login
4. require_admin() adicional valida role == "admin" → 403 si falla
```

## 🗄️ Base de Datos

- **Motor**: SQLite (`users.db`)
- **ORM**: SQLAlchemy 2.0 con **SQL puro** (`text()`)
- **Hashing**: Argon2 via `passlib`
- **Tabla**: `users` con columnas:
  - `id` (INTEGER PRIMARY KEY)
  - `username` (VARCHAR, UNIQUE)
  - `name` (VARCHAR)
  - `hashed_pass` (VARCHAR)
  - `email` (VARCHAR, NULLABLE)
  - `role` (VARCHAR, default: "user")

### Consulta SQL de Ejemplo
```python
result = db.execute(
    text("SELECT username, name, hashed_pass, email, role FROM users WHERE username = :username"),
    {"username": username}
).fetchone()
```

## 👥 Usuarios de Prueba

| Usuario | Contraseña | Rol | Acceso a /admin |
|---------|------------|-----|----------------|
| admin | admin123 | admin | ✅ Sí |
| usuario | pass123 | user | ❌ No (403) |

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.13+
- uv (gestor de dependencias)

### Instalación
```bash
# Instalar dependencias
uv sync

# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

### Ejecutar Servidor

**Opción 1: FastAPI CLI (Recomendado para desarrollo)**
```bash
fastapi dev main.py
```

**Opción 2: Uvicorn**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Opción 3: Producción**
```bash
fastapi run main.py
```

Accede a: **http://127.0.0.1:8000**

## 📚 Documentación API

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Pruebas

### Login como Usuario Normal
1. Ir a http://127.0.0.1:8000/login
2. Ingresar: `usuario` / `pass123`
3. Acceder a `/dashboard`, `/profile`, `/reportes` ✅
4. Intentar acceder a `/admin` → Error 403 ❌

### Login como Admin
1. Ir a http://127.0.0.1:8000/login
2. Ingresar: `admin` / `admin123`
3. Acceder a todas las rutas incluyendo `/admin` ✅

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con **Argon2** (más seguro que bcrypt)
- ✅ Sesiones firmadas con `SECRET_KEY`
- ✅ Validación de roles (RBAC básico)
- ✅ Protección CSRF implícita en sesiones
- ✅ SQL parametrizado (previene SQL injection)
- ⚠️ **Producción**: Cambiar `SECRET_KEY` y usar HTTPS

## 📦 Dependencias Principales

```toml
[project]
dependencies = [
    "fastapi[standard]>=0.121.0",
    "sqlalchemy>=2.0.44",
    "passlib[argon2]>=1.7.4",
    "itsdangerous>=2.2.0",
]
```

## 🛠️ Ventajas de la Arquitectura

1. **Modularidad**: Cada módulo tiene una responsabilidad única
2. **Escalabilidad**: Fácil agregar nuevos routers o servicios
3. **Testabilidad**: Servicios y dependencias fáciles de testear
4. **Mantenibilidad**: Cambios localizados sin efectos colaterales
5. **Tipado Fuerte**: Pydantic valida datos automáticamente
6. **Reutilización**: Dependencias y servicios compartidos

## 📝 Notas Técnicas

### Imports Relativos vs Absolutos
- Se usan **imports relativos** (`.module`) para compatibilidad con `fastapi dev`
- `fastapi dev` ejecuta como paquete: `fastapi-user-auth.main:app`
- `uvicorn` puede usar imports absolutos desde el directorio

### SQL Puro en lugar de ORM
- Uso de `text()` de SQLAlchemy para consultas SQL directas
- Mayor control y transparencia sobre las queries
- Evita la sobrecarga del ORM para operaciones simples

### Dependencias Encadenadas
```python
# require_admin depende de get_current_user automáticamente
@router.get("/admin")
async def admin_panel(admin: Annotated[User, Depends(require_admin)]):
    ...
```

## 📄 Licencia

MIT