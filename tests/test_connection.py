"""
Prueba manual de conexión con MySQL.

Ejecutar desde la raíz del proyecto con:
python -m tests.test_connection
"""

from pymysql import MySQLError

from backend.core.config import settings
from backend.core.database import create_connection


def test_connection() -> None:
    """Comprueba que Python pueda conectarse a MySQL."""

    connection = None

    try:
        connection = create_connection()

        print("Conexión realizada correctamente.")
        print(f"Servidor: {settings.db_host}")
        print(f"Puerto: {settings.db_port}")
        print(f"Base de datos: {settings.db_name}")

    except MySQLError as error:
        print("No fue posible conectar con MySQL.")
        print(f"Detalle: {error}")

    finally:
        if connection is not None:
            connection.close()
            print("Conexión cerrada correctamente.")


if __name__ == "__main__":
    test_connection()