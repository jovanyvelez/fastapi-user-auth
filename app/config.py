"""Configuración de la aplicación"""

from fastapi.templating import Jinja2Templates

# Configuración de seguridad
SECRET_KEY = "d1e15362db01ebee6e3993ad6ddd0352acb4c46c1cc415de4c208922922764b2"

# Templates
templates = Jinja2Templates(directory="templates")
