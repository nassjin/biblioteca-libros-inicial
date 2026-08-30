-- =========================================================
-- BASE DE DATOS: BIBLIOTECA ESCOLAR
-- =========================================================

CREATE DATABASE IF NOT EXISTS biblioteca_escolar
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE biblioteca_escolar;


-- =========================================================
-- TABLA: LIBROS
-- =========================================================

CREATE TABLE IF NOT EXISTS libros (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(120) NOT NULL,
    genero VARCHAR(60) NOT NULL,

    isbn VARCHAR(20) NULL UNIQUE,
    anio_publicacion SMALLINT UNSIGNED NOT NULL,
    ejemplares SMALLINT UNSIGNED NOT NULL DEFAULT 1,

    ubicacion VARCHAR(50) NOT NULL DEFAULT 'Sin asignar',

    estado ENUM(
        'DISPONIBLE',
        'AGOTADO',
        'MANTENCION'
    ) NOT NULL DEFAULT 'DISPONIBLE',

    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    fecha_actualizacion TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT chk_libros_titulo
        CHECK (CHAR_LENGTH(TRIM(titulo)) >= 2),

    CONSTRAINT chk_libros_autor
        CHECK (CHAR_LENGTH(TRIM(autor)) >= 2),

    CONSTRAINT chk_libros_anio
        CHECK (anio_publicacion BETWEEN 1450 AND 2100),

    CONSTRAINT chk_libros_ejemplares
        CHECK (ejemplares >= 0)
);