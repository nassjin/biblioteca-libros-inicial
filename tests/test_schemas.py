"""
Pruebas manuales de los esquemas Pydantic.

Ejecutar con:
python -m tests.test_schemas
"""

from pydantic import ValidationError

from backend.schema.libro_schema import LibroCrear


def probar_libro_correcto() -> None:
    """Prueba la creación de un libro válido."""

    libro = LibroCrear(
        titulo="  El principito  ",
        autor="Antoine de Saint-Exupéry",
        genero="Narrativa",
        isbn="978-0-15601-219-5",
        anio_publicacion=1943,
        ejemplares=4,
        ubicacion="Estante A-01",
        estado="DISPONIBLE",
    )

    print("Libro válido:")
    print(libro.model_dump())


def probar_libro_incorrecto() -> None:
    """Prueba datos que deberían ser rechazados."""

    try:
        LibroCrear(
            titulo="A",
            autor="B",
            genero="",
            isbn="ISBN-INCORRECTO",
            anio_publicacion=1200,
            ejemplares=-3,
            ubicacion="",
            estado="PRESTADO",
        )

    except ValidationError as error:
        print("\nDatos rechazados correctamente:")

        for detalle in error.errors():
            campo = detalle["loc"][0]
            mensaje = detalle["msg"]

            print(f"- {campo}: {mensaje}")


if __name__ == "__main__":
    probar_libro_correcto()
    probar_libro_incorrecto()