# 🔐 Miniproyecto: Sistema de Autenticación Web

## 📝 Descripción del Ejercicio

Vas a crear un **sistema de autenticación web** simple usando FastAPI. El proyecto permite que diferentes usuarios accedan a diferentes páginas según sus permisos.

**⏱️ Duración estimada:** 1 - 1.5 horas

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este ejercicio, habrás aprendido a:

- ✅ Crear una aplicación web con FastAPI
- ✅ Implementar autenticación basada en sesiones
- ✅ Controlar acceso a páginas según el rol del usuario
- ✅ Renderizar plantillas HTML con Jinja2
- ✅ Manejar formularios de login
- ✅ Proteger rutas privadas

---

## 👥 Usuarios del Sistema

El sistema tiene **2 usuarios** con diferentes permisos:

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `user` | `1234` | Usuario normal | ✅ Index (público), ✅ Informe |
| `admon` | `admin` | Administrador | ✅ Todas las páginas (Index, Informe, Admin) |

---

## 📄 Páginas del Sistema

### 1. **Index (/)** - 🌐 Pública
- Accesible sin login
- Página de bienvenida
- Muestra botón "Iniciar Sesión" si no estás autenticado
- Muestra tu nombre y botón "Cerrar Sesión" si estás autenticado

### 2. **Informe (/informe)** - 🔒 Requiere login
- Solo usuarios autenticados (`user` o `admon`)
- Muestra un informe simple
- Si intentas acceder sin login → te redirige a `/login`

### 3. **Admin (/admon)** - 👑 Solo administradores
- Solo el usuario `admon` puede acceder
- Panel de administración
- Si `user` intenta acceder → error 403 (Prohibido)

### 4. **Login (/login)** - 🔑 Formulario
- Formulario con usuario y contraseña
- Valida credenciales
- Crea sesión si las credenciales son correctas
- Muestra error si las credenciales son incorrectas

### 5. **Logout (/logout)** - 🚪 Cerrar sesión
- Elimina la sesión actual
- Redirige a la página de inicio

---

## 🏗️ Estructura del Proyecto

```
project/
├── main.py              # Aplicación principal FastAPI
├── templates/           # Plantillas HTML
│   ├── index.html       # Página de inicio (pública)
│   ├── login.html       # Formulario de login
│   ├── informe.html     # Informe (requiere login)
│   ├── admon.html       # Panel admin (solo admon)
│   └── error_403.html   # Página de error (acceso denegado)
└── README.md           # Documentación
```

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Jinja2**: Motor de plantillas HTML
- **Starlette**: Middleware de sesiones
- **Python 3.13+**

---

## 📋 Pasos para Desarrollar el Proyecto

### **Paso 1: Configuración Inicial (10 min)**

1. Crear la carpeta `project/` y `project/templates/`
2. Crear el archivo `main.py`
3. Importar las librerías necesarias:
   ```python
   from fastapi import FastAPI, Request, Form, Depends, HTTPException
   from fastapi.responses import HTMLResponse, RedirectResponse
   from fastapi.templating import Jinja2Templates
   from starlette.middleware.sessions import SessionMiddleware
   ```

### **Paso 2: Crear la Base de Datos de Usuarios (5 min)**

Crear un diccionario simple con los usuarios:
```python
USERS_DB = {
    "user": {"password": "1234", "role": "user"},
    "admon": {"password": "admin", "role": "admin"}
}
```

### **Paso 3: Configurar FastAPI y Sesiones (5 min)**

```python
app = FastAPI()
SECRET_KEY = "mi-clave-secreta-super-segura"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory="templates")
```

### **Paso 4: Crear Dependencias de Autenticación (15 min)**

Crear funciones para:
- Obtener el usuario actual de la sesión
- Verificar si el usuario está autenticado
- Verificar si el usuario es administrador

### **Paso 5: Crear las Rutas (30 min)**

Implementar las siguientes rutas:

1. **`GET /`** → Página de inicio (pública)
2. **`GET /login`** → Formulario de login
3. **`POST /login`** → Procesar login
4. **`GET /logout`** → Cerrar sesión
5. **`GET /informe`** → Informe (protegida)
6. **`GET /admon`** → Panel admin (solo admin)

### **Paso 6: Crear las Plantillas HTML (25 min)**

Crear 5 archivos HTML básicos:

1. **`index.html`**: Página de bienvenida
2. **`login.html`**: Formulario de login
3. **`informe.html`**: Página de informe
4. **`admon.html`**: Panel de administración
5. **`error_403.html`**: Página de error

---

## 🎨 Diseño de las Plantillas (Ejemplo)

### **login.html** (Ejemplo básico)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; max-width: 400px; margin: 50px auto; }
        input { display: block; width: 100%; margin: 10px 0; padding: 8px; }
        button { padding: 10px 20px; background: blue; color: white; border: none; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>🔐 Iniciar Sesión</h1>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    <form method="post">
        <input type="text" name="username" placeholder="Usuario" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Entrar</button>
    </form>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
```

---

## ✅ Lista de Verificación (Checklist)

Marca cada item cuando lo completes:

- [ ] Configuración inicial de FastAPI
- [ ] Middleware de sesiones configurado
- [ ] Base de datos de usuarios creada
- [ ] Función para obtener usuario actual
- [ ] Función para verificar si es admin
- [ ] Ruta `/` (Index) - pública
- [ ] Ruta `/login` (GET) - formulario
- [ ] Ruta `/login` (POST) - procesar login
- [ ] Ruta `/logout` - cerrar sesión
- [ ] Ruta `/informe` - protegida
- [ ] Ruta `/admon` - solo admin
- [ ] Plantilla `index.html`
- [ ] Plantilla `login.html`
- [ ] Plantilla `informe.html`
- [ ] Plantilla `admon.html`
- [ ] Plantilla `error_403.html`
- [ ] Manejador de error 401 (redirige a login)
- [ ] Manejador de error 403 (acceso denegado)
- [ ] Prueba: Login con `user`
- [ ] Prueba: Login con `admon`
- [ ] Prueba: Acceso a `/informe` sin login
- [ ] Prueba: `user` intenta acceder a `/admon`

---

## 🧪 Pruebas del Sistema

### **Prueba 1: Usuario Normal**
1. Iniciar sesión con `user` / `1234`
2. ✅ Debe poder acceder a `/informe`
3. ❌ Al intentar `/admon` debe ver error 403

### **Prueba 2: Administrador**
1. Iniciar sesión con `admon` / `admin`
2. ✅ Debe poder acceder a `/informe`
3. ✅ Debe poder acceder a `/admon`

### **Prueba 3: Sin Autenticación**
1. Intentar acceder a `/informe` sin login
2. ❌ Debe redirigir a `/login`

---

## 🚀 Ejecutar el Proyecto

```bash
# Instalar FastAPI y Uvicorn
pip install "fastapi[standard]"

# Ejecutar el servidor
uvicorn main:app --reload

# Abrir en el navegador
# http://127.0.0.1:8000
```

---

## 💡 Conceptos Clave

### **¿Qué son las Sesiones?**
Las sesiones permiten que el servidor "recuerde" quién eres entre diferentes peticiones. Es como una ficha que te dan al entrar a un evento para identificarte.

### **¿Qué es un Middleware?**
Es código que se ejecuta antes de procesar cada petición. El middleware de sesiones encripta y desencripta las sesiones automáticamente.

### **¿Qué es una Dependencia en FastAPI?**
Es una función que se ejecuta antes de la ruta para preparar datos. Por ejemplo, verificar si estás autenticado antes de mostrar una página.

### **¿Qué es Jinja2?**
Es un motor de plantillas que permite crear HTML dinámico. Puedes usar variables, condicionales y bucles en HTML.

---

## 🎯 Retos Adicionales (Opcional)

Si terminas antes de tiempo, intenta:

1. **Agregar un tercer usuario** con rol "invitado"
2. **Crear una página de registro** para nuevos usuarios
3. **Agregar estilos CSS** para hacer las páginas más bonitas
4. **Guardar usuarios en un archivo JSON** en lugar de un diccionario
5. **Hashear las contraseñas** con `passlib`
6. **Agregar un contador de visitas** en la página de inicio
7. **Mostrar la fecha y hora** del último login

---

## 📚 Recursos de Ayuda

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Jinja2 Docs**: https://jinja.palletsprojects.com
- **HTML Basics**: https://www.w3schools.com/html

---

## 🏆 Resultado Esperado

Al finalizar, tendrás un **sistema de autenticación funcional** donde:

✅ Los usuarios pueden iniciar sesión  
✅ Las páginas están protegidas según el rol  
✅ El administrador tiene acceso completo  
✅ Los usuarios normales tienen acceso limitado  
✅ Las sesiones se manejan de forma segura  

---

## 👨‍🏫 Para el Instructor

### **Tiempo Estimado por Sección**
- Configuración: 10 min
- Base de datos: 5 min
- Autenticación: 15 min
- Rutas: 30 min
- Plantillas: 25 min
- Pruebas: 10 min
- **Total: ~95 minutos**

### **Dificultad**
⭐⭐⭐ Intermedio

### **Prerrequisitos**
- Python básico
- HTML básico
- Conceptos de HTTP (GET, POST)

### **Puntos de Enseñanza Clave**
1. Seguridad web básica
2. Autenticación vs Autorización
3. Sesiones y cookies
4. Protección de rutas
5. Plantillas dinámicas

---

¡Buena suerte con tu proyecto! 🚀
