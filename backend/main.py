"""
Punto de entrada de la API Biblioteca Escolar.
"""

from fastapi import FastAPI
from backend.routes.libros import router as libros_router

app = FastAPI(
    title="API Biblioteca Escolar",
    description=(
        "API REST para administrar el catálogo de una "
        "biblioteca escolar."
    ),
    version="2.0.0",
)

app.include_router(libros_router)

@app.get(
    "/",
    tags=["Estado"],
)
def comprobar_api() -> dict[str, str]:
    """Comprueba que la API esté funcionando."""

    return {
        "estado": "ok",
        "mensaje": "La API Biblioteca Escolar está funcionando.",
    }