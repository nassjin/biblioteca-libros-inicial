"""Validación de los datos de libros."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EstadoLibro(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    MANTENCION = "MANTENCION"


class LibroCrear(BaseModel):
    titulo: str = Field(min_length=2, max_length=150)
    autor: str = Field(min_length=2, max_length=120)
    genero: str = Field(min_length=2, max_length=60)
    isbn: str | None = Field(default=None, max_length=20)
    anio_publicacion: int = Field(ge=1450, le=2100)
    ejemplares: int = Field(ge=0)
    ubicacion: str = Field(default="Sin asignar", max_length=50)
    estado: EstadoLibro = EstadoLibro.DISPONIBLE


class LibroActualizar(BaseModel):
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
    isbn: str | None = Field(default=None, max_length=20)
    anio_publicacion: int | None = Field(
        default=None,
        ge=1450,
        le=2100,
    )
    ejemplares: int | None = Field(default=None, ge=0)
    ubicacion: str | None = Field(default=None, max_length=50)
    estado: EstadoLibro | None = None


class LibroRespuesta(LibroCrear):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime