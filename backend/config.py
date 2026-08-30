"""
Configuración general del backend.

Las credenciales se obtienen desde el archivo .env para evitar
escribir contraseñas directamente en el código.
"""

import os

from dotenv import load_dotenv


# Carga las variables guardadas en el archivo .env.
load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "biblioteca_escolar")