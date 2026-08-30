-- =========================================================
-- TRIGGERS DE LA BIBLIOTECA ESCOLAR
-- =========================================================

USE biblioteca_escolar;


-- Eliminamos los triggers anteriores si ya existen.
DROP TRIGGER IF EXISTS trg_libros_before_insert;
DROP TRIGGER IF EXISTS trg_libros_before_update;


-- =========================================================
-- TRIGGER ANTES DE INSERTAR
-- =========================================================

DELIMITER $$

CREATE TRIGGER trg_libros_before_insert
BEFORE INSERT ON libros
FOR EACH ROW
BEGIN
    -- Elimina espacios al inicio y al final.
    SET NEW.titulo = TRIM(NEW.titulo);
    SET NEW.autor = TRIM(NEW.autor);
    SET NEW.genero = TRIM(NEW.genero);
    SET NEW.ubicacion = TRIM(NEW.ubicacion);

    -- Elimina espacios y guiones del ISBN.
    IF NEW.isbn IS NOT NULL THEN
        SET NEW.isbn = REPLACE(NEW.isbn, '-', '');
        SET NEW.isbn = REPLACE(NEW.isbn, ' ', '');
        SET NEW.isbn = NULLIF(TRIM(NEW.isbn), '');
    END IF;

    -- Sincroniza el estado, excepto cuando está en mantención.
    IF NEW.estado <> 'MANTENCION' THEN
        IF NEW.ejemplares = 0 THEN
            SET NEW.estado = 'AGOTADO';
        ELSE
            SET NEW.estado = 'DISPONIBLE';
        END IF;
    END IF;
END$$


-- =========================================================
-- TRIGGER ANTES DE ACTUALIZAR
-- =========================================================

CREATE TRIGGER trg_libros_before_update
BEFORE UPDATE ON libros
FOR EACH ROW
BEGIN
    -- Elimina espacios al inicio y al final.
    SET NEW.titulo = TRIM(NEW.titulo);
    SET NEW.autor = TRIM(NEW.autor);
    SET NEW.genero = TRIM(NEW.genero);
    SET NEW.ubicacion = TRIM(NEW.ubicacion);

    -- Elimina espacios y guiones del ISBN.
    IF NEW.isbn IS NOT NULL THEN
        SET NEW.isbn = REPLACE(NEW.isbn, '-', '');
        SET NEW.isbn = REPLACE(NEW.isbn, ' ', '');
        SET NEW.isbn = NULLIF(TRIM(NEW.isbn), '');
    END IF;

    -- Sincroniza el estado, excepto cuando está en mantención.
    IF NEW.estado <> 'MANTENCION' THEN
        IF NEW.ejemplares = 0 THEN
            SET NEW.estado = 'AGOTADO';
        ELSE
            SET NEW.estado = 'DISPONIBLE';
        END IF;
    END IF;
END$$

DELIMITER ;