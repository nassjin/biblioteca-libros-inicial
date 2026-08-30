-- =========================================================
-- DATOS INICIALES PARA PRUEBAS
-- =========================================================

USE biblioteca_escolar;


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
VALUES
    (
        'El principito',
        'Antoine de Saint-Exupéry',
        'Narrativa',
        '9780156012195',
        1943,
        4,
        'Estante A-01',
        'DISPONIBLE'
    ),
    (
        'Subterra',
        'Baldomero Lillo',
        'Cuento',
        '9789561234567',
        1904,
        2,
        'Estante B-03',
        'DISPONIBLE'
    ),
    (
        'Cien años de soledad',
        'Gabriel García Márquez',
        'Realismo mágico',
        '9780307474728',
        1967,
        0,
        'Estante C-02',
        'AGOTADO'
    ),
    (
        'Papelucho',
        'Marcela Paz',
        'Infantil',
        '9789561123458',
        1947,
        3,
        'Estante I-04',
        'DISPONIBLE'
    );