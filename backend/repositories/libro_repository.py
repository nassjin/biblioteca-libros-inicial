"""
Repositorio de libros.

Este módulo contiene todas las consultas SQL relacionadas
con la tabla libros.
"""

from typing import Any
from backend.core.database import get_database


# Columnas que se permite modificar.
# Esta lista evita incorporar nombres de columnas desconocidos
# en una consulta UPDATE.
UPDATE_FIELDS = {
    "titulo",
    "autor",
    "genero",
    "isbn",
    "anio_publicacion",
    "ejemplares",
    "ubicacion",
    "estado",
}


def list_books() -> list[dict[str, Any]]:
    """Obtiene todos los libros ordenados por título."""

    query = """
        SELECT
            id,
            titulo,
            autor,
            genero,
            isbn,
            anio_publicacion,
            ejemplares,
            ubicacion,
            estado,
            fecha_creacion,
            fecha_actualizacion
        FROM libros
        ORDER BY titulo ASC
    """

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_book_by_id(book_id: int) -> dict[str, Any] | None:
    """Obtiene un libro mediante su identificador."""

    query = """
        SELECT
            id,
            titulo,
            autor,
            genero,
            isbn,
            anio_publicacion,
            ejemplares,
            ubicacion,
            estado,
            fecha_creacion,
            fecha_actualizacion
        FROM libros
        WHERE id = %s
    """

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (book_id,))
            return cursor.fetchone()


def search_books(search_text: str) -> list[dict[str, Any]]:
    """Busca libros por título, autor, género o ISBN."""

    query = """
        SELECT
            id,
            titulo,
            autor,
            genero,
            isbn,
            anio_publicacion,
            ejemplares,
            ubicacion,
            estado,
            fecha_creacion,
            fecha_actualizacion
        FROM libros
        WHERE titulo LIKE %s
           OR autor LIKE %s
           OR genero LIKE %s
           OR isbn LIKE %s
        ORDER BY titulo ASC
    """

    search_pattern = f"%{search_text}%"

    parameters = (
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
    )

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()


def get_book_by_isbn(isbn: str) -> dict[str, Any] | None:
    """Busca un libro mediante su ISBN."""

    query = """
        SELECT
            id,
            titulo,
            autor,
            genero,
            isbn,
            anio_publicacion,
            ejemplares,
            ubicacion,
            estado,
            fecha_creacion,
            fecha_actualizacion
        FROM libros
        WHERE isbn = %s
    """

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (isbn,))
            return cursor.fetchone()


def create_book(book_data: dict[str, Any]) -> dict[str, Any] | None:
    """Registra un libro y devuelve el registro creado."""

    query = """
        INSERT INTO libros (
            titulo,
            autor,
            genero,
            isbn,
            anio_publicacion,
            ejemplares,
            ubicacion,
            estado
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    parameters = (
        book_data["titulo"],
        book_data["autor"],
        book_data["genero"],
        book_data.get("isbn"),
        book_data["anio_publicacion"],
        book_data["ejemplares"],
        book_data["ubicacion"],
        book_data["estado"],
    )

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            book_id = cursor.lastrowid

    return get_book_by_id(book_id)


def update_book(
    book_id: int,
    book_data: dict[str, Any],
) -> dict[str, Any] | None:
    """Actualiza los campos recibidos de un libro."""

    safe_data = {
        field: value
        for field, value in book_data.items()
        if field in UPDATE_FIELDS
    }

    if not safe_data:
        return get_book_by_id(book_id)

    assignments = ", ".join(
        f"{field} = %s"
        for field in safe_data
    )

    query = f"""
        UPDATE libros
        SET {assignments}
        WHERE id = %s
    """

    parameters = tuple(safe_data.values()) + (book_id,)

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)

    return get_book_by_id(book_id)


def delete_book(book_id: int) -> bool:
    """Elimina un libro y devuelve True si existía."""

    query = """
        DELETE FROM libros
        WHERE id = %s
    """

    with get_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (book_id,))
            deleted_rows = cursor.rowcount

    return deleted_rows > 0