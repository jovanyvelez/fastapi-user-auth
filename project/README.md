# 🔐 Sistema de Autenticación Simple

Miniproyecto educativo para aprender autenticación web con FastAPI.

## 📝 Descripción

Este es un sistema de autenticación básico que demuestra:
- Autenticación basada en sesiones
- Control de acceso por roles
- Protección de rutas
- Manejo de permisos

## 👥 Usuarios del Sistema

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `user` | `1234` | Usuario normal | ✅ Index, ✅ Informe |
| `admon` | `admin` | Administrador | ✅ Todas las páginas |

## 📄 Páginas

- **`/`** - Inicio (pública)
- **`/login`** - Formulario de login
- **`/logout`** - Cerrar sesión
- **`/informe`** - Informe (requiere login)
- **`/admon`** - Panel admin (solo administradores)

## 🚀 Ejecutar el Proyecto

### Requisitos
- Python 3.13+
- FastAPI

### Instalación

```bash
# Instalar FastAPI
pip install "fastapi[standard]"
```

### Ejecutar

```bash
# Opción 1: Uvicorn
uvicorn main:app --reload

# Opción 2: FastAPI CLI
fastapi dev main.py
```

Abrir en el navegador: **http://127.0.0.1:8000**

## 🧪 Pruebas

### Prueba 1: Usuario Normal
1. Login: `user` / `1234`
2. ✅ Acceso a `/informe`
3. ❌ Error 403 al intentar `/admon`

### Prueba 2: Administrador
1. Login: `admon` / `admin`
2. ✅ Acceso a `/informe`
3. ✅ Acceso a `/admon`

### Prueba 3: Sin Login
1. Intentar acceder a `/informe`
2. ❌ Redirige a `/login`

## 🏗️ Estructura del Código

```python
# Usuarios en memoria
USERS_DB = {
    "user": {"password": "1234", "role": "user"},
    "admon": {"password": "admin", "role": "admin"}
}

# Dependencias de autenticación
def get_current_user(request) -> dict
def require_admin(user) -> dict

# Rutas
GET  /           → Página de inicio (pública)
GET  /login      → Formulario de login
POST /login      → Procesar login
GET  /logout     → Cerrar sesión
GET  /informe    → Informe (protegida)
GET  /admon      → Admin (solo admin)
```

## 🔒 Seguridad

- Sesiones encriptadas con `SECRET_KEY`
- Protección de rutas con dependencias
- Control de acceso basado en roles (RBAC)
- Redirección automática para usuarios no autenticados

## 📚 Conceptos Aprendidos

1. **Sesiones**: Almacenar información del usuario entre peticiones
2. **Middleware**: Código que se ejecuta antes de cada petición
3. **Dependencias**: Funciones que preparan datos para las rutas
4. **Plantillas**: HTML dinámico con Jinja2
5. **Autenticación vs Autorización**: Verificar identidad vs permisos

## 🎯 Mejoras Posibles

- [ ] Agregar más usuarios
- [ ] Crear página de registro
- [ ] Hashear contraseñas con `passlib`
- [ ] Guardar usuarios en archivo JSON
- [ ] Agregar estilos CSS personalizados
- [ ] Implementar "recordar sesión"
- [ ] Agregar validación de formularios

---

**Creado como ejercicio educativo** 🚀
