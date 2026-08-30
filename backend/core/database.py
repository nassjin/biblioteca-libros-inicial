"""
Conexión con la base de datos MySQL.

Este módulo centraliza la creación y el cierre de conexiones
para evitar repetir la configuración en diferentes archivos.
"""

from contextlib import contextmanager
from typing import Generator

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from backend.core.config import settings


def create_connection() -> Connection:
    """
    Abre una conexión nueva con MySQL.

    DictCursor permite recibir cada registro como diccionario.
    Por ejemplo: {"id": 1, "titulo": "El principito"}.
    """

    return pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


@contextmanager
def get_database() -> Generator[Connection, None, None]:
    """
    Entrega una conexión y garantiza que siempre sea cerrada.

    Si las operaciones se completan correctamente, confirma
    los cambios mediante commit. Si ocurre un error, utiliza
    rollback para deshacer la operación incompleta.
    """

    connection = create_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()