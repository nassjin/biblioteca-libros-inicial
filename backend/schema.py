"""
Esquemas de validación para los libros.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class EstadoLibro(str, Enum):
    """Estados permitidos para un libro."""

    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    MANTENCION = "MANTENCION"


class LibroCrear(BaseModel):
    """Datos necesarios para registrar un libro."""

    titulo: str = Field(
        min_length=2,
        max_length=150,
    )

    autor: str = Field(
        min_length=2,
        max_length=120,
    )

    genero: str = Field(
        min_length=2,
        max_length=60,
    )

    isbn: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
    )

    anio_publicacion: int = Field(
        ge=1450,
        le=2100,
    )

    ejemplares: int = Field(
        ge=0,
        le=10000,
    )

    ubicacion: str = Field(
        default="Sin asignar",
        min_length=2,
        max_length=50,
    )

    estado: EstadoLibro = EstadoLibro.DISPONIBLE

    @field_validator(
        "titulo",
        "autor",
        "genero",
        "ubicacion",
        mode="before",
    )
    @classmethod
    def limpiar_texto(cls, valor: str) -> str:
        """Elimina espacios innecesarios."""

        if isinstance(valor, str):
            return valor.strip()

        return valor

    @field_validator("isbn", mode="before")
    @classmethod
    def validar_isbn(
        cls,
        valor: str | None,
    ) -> str | None:
        """Limpia y valida el ISBN."""

        if valor is None:
            return None

        isbn = str(valor).strip()
        isbn = isbn.replace("-", "").replace(" ", "")

        if not isbn:
            return None

        if not isbn.isdigit():
            raise ValueError(
                "El ISBN solamente puede contener números"
            )

        return isbn


class LibroActualizar(BaseModel):
    """Datos que se pueden modificar de un libro."""

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
    def limpiar_texto(
        cls,
        valor: str | None,
    ) -> str | None:
        """Elimina espacios innecesarios."""

        if isinstance(valor, str):
            return valor.strip()

        return valor

    @field_validator("isbn", mode="before")
    @classmethod
    def validar_isbn(
        cls,
        valor: str | None,
    ) -> str | None:
        """Limpia y valida el ISBN."""

        if valor is None:
            return None

        isbn = str(valor).strip()
        isbn = isbn.replace("-", "").replace(" ", "")

        if not isbn:
            return None

        if not isbn.isdigit():
            raise ValueError(
                "El ISBN solamente puede contener números"
            )

        return isbn


class LibroRespuesta(BaseModel):
    """Estructura utilizada al devolver un libro."""

    id: int
    titulo: str
    autor: str
    genero: str
    isbn: str | None
    anio_publicacion: int
    ejemplares: int
    ubicacion: str
    estado: EstadoLibro
    fecha_creacion: datetime
    fecha_actualizacion: datetime