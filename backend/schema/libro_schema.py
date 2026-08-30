"""
Esquemas de validación para los libros.

Los esquemas determinan qué datos acepta la API y qué datos
devuelve al frontend.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class EstadoLibro(str, Enum):
    """Estados permitidos para un libro."""

    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    MANTENCION = "MANTENCION"


class LibroBase(BaseModel):
    """Campos compartidos al crear y mostrar un libro."""

    titulo: str = Field(
        min_length=2,
        max_length=150,
        examples=["El principito"],
    )

    autor: str = Field(
        min_length=2,
        max_length=120,
        examples=["Antoine de Saint-Exupéry"],
    )

    genero: str = Field(
        min_length=2,
        max_length=60,
        examples=["Narrativa"],
    )

    isbn: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
        examples=["9780156012195"],
    )

    anio_publicacion: int = Field(
        ge=1450,
        le=2100,
        examples=[1943],
    )

    ejemplares: int = Field(
        ge=0,
        le=10000,
        examples=[4],
    )

    ubicacion: str = Field(
        default="Sin asignar",
        min_length=2,
        max_length=50,
        examples=["Estante A-01"],
    )

    estado: EstadoLibro = Field(
        default=EstadoLibro.DISPONIBLE,
        examples=[EstadoLibro.DISPONIBLE],
    )

    @field_validator(
        "titulo",
        "autor",
        "genero",
        "ubicacion",
        mode="before",
    )
    @classmethod
    def limpiar_textos(cls, valor: str) -> str:
        """Elimina espacios innecesarios al inicio y al final."""

        if isinstance(valor, str):
            return valor.strip()

        return valor

    @field_validator("isbn", mode="before")
    @classmethod
    def limpiar_isbn(cls, valor: str | None) -> str | None:
        """
        Limpia el ISBN.

        Un campo vacío se convierte en None porque el ISBN
        es opcional.
        """

        if valor is None:
            return None

        isbn_limpio = str(valor).strip().replace("-", "").replace(" ", "")

        if not isbn_limpio:
            return None

        if not isbn_limpio.isdigit():
            raise ValueError("El ISBN solamente puede contener números")

        return isbn_limpio


class LibroCrear(LibroBase):
    """Datos exigidos para registrar un libro."""

    pass


class LibroActualizar(BaseModel):
    """
    Datos permitidos al actualizar un libro.

    Todos los campos son opcionales porque se puede modificar
    solamente una parte del registro.
    """

    titulo: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    autor: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    genero: str | None = Field(
        default=None,
        min_length=2,
        max_length=60,
    )

    isbn: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
    )

    anio_publicacion: int | None = Field(
        default=None,
        ge=1450,
        le=2100,
    )

    ejemplares: int | None = Field(
        default=None,
        ge=0,
        le=10000,
    )

    ubicacion: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    estado: EstadoLibro | None = None

    @field_validator(
        "titulo",
        "autor",
        "genero",
        "ubicacion",
        mode="before",
    )
    @classmethod
    def limpiar_textos_opcionales(
        cls,
        valor: str | None,
    ) -> str | None:
        """Limpia los campos de texto enviados al actualizar."""

        if isinstance(valor, str):
            return valor.strip()

        return valor

    @field_validator("isbn", mode="before")
    @classmethod
    def limpiar_isbn_opcional(
        cls,
        valor: str | None,
    ) -> str | None:
        """Limpia y comprueba el ISBN durante una actualización."""

        if valor is None:
            return None

        isbn_limpio = str(valor).strip().replace("-", "").replace(" ", "")

        if not isbn_limpio:
            return None

        if not isbn_limpio.isdigit():
            raise ValueError("El ISBN solamente puede contener números")

        return isbn_limpio


class LibroRespuesta(LibroBase):
    """Representa un libro devuelto por la API."""

    id: int
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)