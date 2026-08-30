"""
Conexión con la base de datos MySQL.
"""

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from backend.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)


def get_connection() -> Connection:
    """
    Abre y devuelve una conexión nueva con MySQL.

    DictCursor hace que cada fila se reciba como diccionario.
    """

    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=DictCursor,
    )