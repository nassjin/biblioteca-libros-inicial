"""
Pruebas manuales del repositorio de libros.

Ejecutar con:
python -m tests.test_repository
"""

from backend.repositories.libro_repository import (
    create_book,
    delete_book,
    get_book_by_id,
    list_books,
    search_books,
    update_book,
)


def test_repository() -> None:
    """Ejecuta las operaciones principales del repositorio."""

    print("\n1. LIBROS EXISTENTES")

    books = list_books()

    for book in books:
        print(
            f'{book["id"]}: '
            f'{book["titulo"]} - '
            f'{book["autor"]}'
        )

    print("\n2. CREAR LIBRO")

    new_book = create_book(
        {
            "titulo": "La amortajada",
            "autor": "María Luisa Bombal",
            "genero": "Novela",
            "isbn": "9789560000125",
            "anio_publicacion": 1938,
            "ejemplares": 2,
            "ubicacion": "Estante C-05",
            "estado": "DISPONIBLE",
        }
    )

    if new_book is None:
        print("No fue posible crear el libro.")
        return

    book_id = new_book["id"]
    print(f"Libro creado con ID {book_id}")
    print(new_book)

    print("\n3. BUSCAR POR ID")

    found_book = get_book_by_id(book_id)
    print(found_book)

    print("\n4. BUSCAR POR TEXTO")

    results = search_books("Bombal")

    for book in results:
        print(book)

    print("\n5. ACTUALIZAR")

    updated_book = update_book(
        book_id,
        {
            "ejemplares": 5,
            "ubicacion": "Estante CH-02",
        },
    )

    print(updated_book)

    print("\n6. ELIMINAR")

    was_deleted = delete_book(book_id)
    print(f"Libro eliminado: {was_deleted}")

    print("\n7. COMPROBAR ELIMINACIÓN")

    deleted_book = get_book_by_id(book_id)
    print(deleted_book)


if __name__ == "__main__":
    test_repository()