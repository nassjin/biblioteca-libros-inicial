"""
Endpoints para administrar libros.

Operaciones disponibles:
- Listar
- Buscar
- Obtener por ID
- Crear
- Actualizar
- Eliminar
"""

from typing import Any

from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from pymysql.err import IntegrityError, MySQLError

from backend.database import get_connection
from backend.schema import (
    LibroActualizar,
    LibroCrear,
    LibroRespuesta,
)


router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
)


@router.get(
    "/",
    response_model=list[LibroRespuesta],
)
def listar_libros() -> list[dict[str, Any]]:
    """Devuelve todos los libros ordenados por título."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM libros
                ORDER BY titulo ASC
                """
            )

            return cursor.fetchall()

    finally:
        connection.close()


@router.get(
    "/buscar/",
    response_model=list[LibroRespuesta],
)
def buscar_libros(
    texto: str = Query(
        min_length=2,
        description="Título, autor, género o ISBN",
    ),
) -> list[dict[str, Any]]:
    """Busca libros utilizando coincidencias parciales."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            patron = f"%{texto.strip()}%"

            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE titulo LIKE %s
                   OR autor LIKE %s
                   OR genero LIKE %s
                   OR isbn LIKE %s
                ORDER BY titulo ASC
                """,
                (
                    patron,
                    patron,
                    patron,
                    patron,
                ),
            )

            return cursor.fetchall()

    finally:
        connection.close()


@router.get(
    "/{libro_id}",
    response_model=LibroRespuesta,
)
def obtener_libro(
    libro_id: int = Path(gt=0),
) -> dict[str, Any]:
    """Obtiene un libro mediante su ID."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE id = %s
                """,
                (libro_id,),
            )

            libro = cursor.fetchone()

    finally:
        connection.close()

    if libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado.",
        )

    return libro


@router.post(
    "/",
    response_model=LibroRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_libro(
    datos: LibroCrear,
) -> dict[str, Any]:
    """Registra un libro nuevo."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            libro = datos.model_dump(mode="json")

            cursor.execute(
                """
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
                """,
                (
                    libro["titulo"],
                    libro["autor"],
                    libro["genero"],
                    libro["isbn"],
                    libro["anio_publicacion"],
                    libro["ejemplares"],
                    libro["ubicacion"],
                    libro["estado"],
                ),
            )

            libro_id = cursor.lastrowid
            connection.commit()

            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE id = %s
                """,
                (libro_id,),
            )

            libro_creado = cursor.fetchone()

        return libro_creado

    except IntegrityError as error:
        connection.rollback()

        if error.args[0] == 1062:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un libro con ese ISBN.",
            ) from error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible registrar el libro.",
        ) from error

    except MySQLError as error:
        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al guardar el libro.",
        ) from error

    finally:
        connection.close()


@router.put(
    "/{libro_id}",
    response_model=LibroRespuesta,
)
def actualizar_libro(
    datos: LibroActualizar,
    libro_id: int = Path(gt=0),
) -> dict[str, Any]:
    """Actualiza uno o más campos de un libro."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE id = %s
                """,
                (libro_id,),
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Libro no encontrado.",
                )

            cambios = datos.model_dump(
                mode="json",
                exclude_unset=True,
            )

            if not cambios:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar.",
                )

            columnas_permitidas = {
                "titulo",
                "autor",
                "genero",
                "isbn",
                "anio_publicacion",
                "ejemplares",
                "ubicacion",
                "estado",
            }

            cambios = {
                columna: valor
                for columna, valor in cambios.items()
                if columna in columnas_permitidas
            }

            asignaciones = ", ".join(
                f"{columna} = %s"
                for columna in cambios
            )

            valores = tuple(cambios.values()) + (libro_id,)

            cursor.execute(
                f"""
                UPDATE libros
                SET {asignaciones}
                WHERE id = %s
                """,
                valores,
            )

            connection.commit()

            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE id = %s
                """,
                (libro_id,),
            )

            libro_actualizado = cursor.fetchone()

        return libro_actualizado

    except IntegrityError as error:
        connection.rollback()

        if error.args[0] == 1062:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe otro libro con ese ISBN.",
            ) from error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible actualizar el libro.",
        ) from error

    except MySQLError as error:
        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el libro.",
        ) from error

    finally:
        connection.close()


@router.delete(
    "/{libro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_libro(
    libro_id: int = Path(gt=0),
) -> Response:
    """Elimina un libro mediante su ID."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM libros
                WHERE id = %s
                """,
                (libro_id,),
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Libro no encontrado.",
                )

            connection.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except MySQLError as error:
        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el libro.",
        ) from error

    finally:
        connection.close()