"""
Configuración general del backend.

Este módulo obtiene las variables del archivo .env y las reúne
en un único objeto de configuración.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Busca el archivo .env y carga sus variables.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Representa la configuración utilizada por la aplicación.
    frozen=True evita modificar accidentalmente estos valores
    mientras el programa está funcionando.
    """

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    api_host: str
    api_port: int


def get_settings() -> Settings:
    """Construye la configuración usando las variables de entorno."""

    return Settings(
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "3306")),
        db_user=os.getenv("DB_USER", "root"),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_name=os.getenv("DB_NAME", "biblioteca_escolar"),
        api_host=os.getenv("API_HOST", "127.0.0.1"),
        api_port=int(os.getenv("API_PORT", "8000")),
    )


# Se crea una sola configuración para todo el backend.
settings = get_settings()