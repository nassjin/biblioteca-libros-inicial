"""
Interfaz gráfica de la Biblioteca Escolar.

El frontend utiliza Flet y se comunica con FastAPI
mediante peticiones HTTP.
"""

import os
import flet as ft
import requests
from dotenv import load_dotenv

# ==========================================================
# CONFIGURACIÓN DE LA API
# ==========================================================

# Carga las variables del archivo .env.
load_dotenv()

BASE_API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

API_URL = f"{BASE_API_URL}/libros/"


def main(page: ft.Page):
    """Construye y controla la interfaz de la biblioteca."""

    # ======================================================
    # CONFIGURACIÓN DE LA PÁGINA
    # ======================================================

    page.title = "Biblioteca Escolar"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.scroll = ft.ScrollMode.AUTO

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
    )

    # Guarda el ID del libro que se está editando.
    libro_id_edicion = None


    # ======================================================
    # CAMPOS DEL FORMULARIO
    # ======================================================

    txt_titulo = ft.TextField(
        label="Título",
        prefix_icon=ft.Icons.BOOK,
        expand=True,
    )

    txt_autor = ft.TextField(
        label="Autor",
        prefix_icon=ft.Icons.PERSON,
        expand=True,
    )

    txt_genero = ft.TextField(
        label="Género",
        prefix_icon=ft.Icons.CATEGORY,
        expand=True,
    )

    txt_isbn = ft.TextField(
        label="ISBN",
        prefix_icon=ft.Icons.NUMBERS,
        hint_text="Puede dejarse vacío",
        expand=True,
    )

    txt_anio = ft.TextField(
        label="Año de publicación",
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )

    txt_ejemplares = ft.TextField(
        label="Número de ejemplares",
        prefix_icon=ft.Icons.INVENTORY_2,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )

    txt_ubicacion = ft.TextField(
        label="Ubicación",
        prefix_icon=ft.Icons.SHELVES,
        hint_text="Ejemplo: Estante A-01",
        expand=True,
    )

    dd_estado = ft.Dropdown(
        label="Estado",
        value="DISPONIBLE",
        options=[
            ft.DropdownOption(
                key="DISPONIBLE",
                text="Disponible",
            ),
            ft.DropdownOption(
                key="AGOTADO",
                text="Agotado",
            ),
            ft.DropdownOption(
                key="MANTENCION",
                text="Mantención",
            ),
        ],
        expand=True,
    )

    txt_buscar = ft.TextField(
        label="Buscar libro",
        hint_text="Título, autor, género o ISBN",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
    )


    # ======================================================
    # TABLA DE LIBROS
    # ======================================================

    tabla = ft.DataTable(
        heading_row_color="#334155",
        data_row_color="#1E293B",
        divider_thickness=0.5,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("ISBN")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Ejemplares")),
            ft.DataColumn(ft.Text("Ubicación")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
    )

    # ======================================================
    # INDICADORES DEL CATÁLOGO
    # ======================================================

    txt_total = ft.Text(
        "0",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.INDIGO_300,
    )

    txt_disponibles = ft.Text(
        "0",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_300,
    )

    txt_agotados = ft.Text(
        "0",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_300,
    )

    txt_mantencion = ft.Text(
        "0",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ORANGE_300,
    )

    def crear_tarjeta_indicador(
            titulo: str,
            valor: ft.Text,
            icono,
            color_fondo: str,
            color_icono,
    ):
        """Crea una tarjeta oscura para un indicador."""

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icono,
                            color=color_icono,
                            size=28,
                        ),
                        padding=12,
                        bgcolor="#1E293B",
                        border_radius=12,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                size=13,
                                color=ft.Colors.GREY_300,
                            ),
                            valor,
                        ],
                        spacing=0,
                    ),
                ],
            ),
            padding=16,
            bgcolor=color_fondo,
            border_radius=16,
            expand=True,
        )

    tarjeta_total = crear_tarjeta_indicador(
        titulo="Total de libros",
        valor=txt_total,
        icono=ft.Icons.LIBRARY_BOOKS,
        color_fondo="#1E1B4B",
        color_icono=ft.Colors.INDIGO_300,
    )

    tarjeta_disponibles = crear_tarjeta_indicador(
        titulo="Disponibles",
        valor=txt_disponibles,
        icono=ft.Icons.CHECK_CIRCLE,
        color_fondo="#052E16",
        color_icono=ft.Colors.GREEN_300,
    )

    tarjeta_agotados = crear_tarjeta_indicador(
        titulo="Agotados",
        valor=txt_agotados,
        icono=ft.Icons.REMOVE_CIRCLE,
        color_fondo="#450A0A",
        color_icono=ft.Colors.RED_300,
    )

    tarjeta_mantencion = crear_tarjeta_indicador(
        titulo="En mantención",
        valor=txt_mantencion,
        icono=ft.Icons.BUILD_CIRCLE,
        color_fondo="#431407",
        color_icono=ft.Colors.ORANGE_300,
    )



    # ======================================================
    # MOSTRAR MENSAJES
    # ======================================================

    def mostrar_mensaje(
        texto: str,
        es_error: bool = False,
    ):
        """Muestra una notificación de éxito o error."""

        mensaje = ft.SnackBar(
            content=ft.Text(
                texto,
                color=ft.Colors.WHITE,
            ),
            bgcolor=(
                ft.Colors.RED_600
                if es_error
                else ft.Colors.GREEN_600
            ),
        )

        page.show_dialog(mensaje)



    # ======================================================
    # OBTENER ERRORES DE FASTAPI
    # ======================================================

    def obtener_error(respuesta: requests.Response) -> str:
        """Obtiene el detalle de un error enviado por FastAPI."""

        try:
            contenido = respuesta.json()
            detalle = contenido.get("detail")

            if isinstance(detalle, str):
                return detalle

            if isinstance(detalle, list):
                mensajes = []

                for error in detalle:
                    campo = error.get("loc", ["campo"])[-1]
                    mensaje = error.get(
                        "msg",
                        "Valor incorrecto",
                    )

                    mensajes.append(
                        f"{campo}: {mensaje}"
                    )

                return "\n".join(mensajes)

        except requests.JSONDecodeError:
            pass

        return "Ocurrió un error inesperado."


    # ======================================================
    # LIMPIAR EL FORMULARIO
    # ======================================================

    def limpiar_formulario():
        """Limpia los campos y finaliza la edición."""

        nonlocal libro_id_edicion

        libro_id_edicion = None

        txt_titulo.value = ""
        txt_autor.value = ""
        txt_genero.value = ""
        txt_isbn.value = ""
        txt_anio.value = ""
        txt_ejemplares.value = ""
        txt_ubicacion.value = ""
        dd_estado.value = "DISPONIBLE"

        btn_guardar.text = "Guardar libro"
        btn_guardar.icon = ft.Icons.SAVE
        btn_cancelar.visible = False

        page.update()


    # ======================================================
    # VALIDAR EL FORMULARIO
    # ======================================================

    def validar_formulario() -> bool:
        """Comprueba que los campos principales sean válidos."""

        campos_obligatorios = [
            txt_titulo.value,
            txt_autor.value,
            txt_genero.value,
            txt_anio.value,
            txt_ejemplares.value,
            txt_ubicacion.value,
            dd_estado.value,
        ]

        if not all(campos_obligatorios):
            mostrar_mensaje(
                "Completa todos los campos obligatorios.",
                es_error=True,
            )
            return False

        try:
            anio = int(txt_anio.value)
            ejemplares = int(txt_ejemplares.value)

        except ValueError:
            mostrar_mensaje(
                "El año y los ejemplares deben ser números enteros.",
                es_error=True,
            )
            return False

        if anio < 1450 or anio > 2100:
            mostrar_mensaje(
                "El año debe estar entre 1450 y 2100.",
                es_error=True,
            )
            return False

        if ejemplares < 0:
            mostrar_mensaje(
                "Los ejemplares no pueden ser negativos.",
                es_error=True,
            )
            return False

        return True


    # ======================================================
    # OBTENER DATOS DEL FORMULARIO
    # ======================================================

    def obtener_datos_formulario() -> dict:
        """Convierte los campos en un diccionario."""

        isbn = txt_isbn.value.strip()

        return {
            "titulo": txt_titulo.value.strip(),
            "autor": txt_autor.value.strip(),
            "genero": txt_genero.value.strip(),

            # Si está vacío, enviamos null a FastAPI.
            "isbn": isbn if isbn else None,

            "anio_publicacion": int(txt_anio.value),
            "ejemplares": int(txt_ejemplares.value),
            "ubicacion": txt_ubicacion.value.strip(),
            "estado": dd_estado.value,
        }

    def crear_etiqueta_estado(estado: str):
        """Crea una etiqueta oscura según el estado."""

        configuracion = {
            "DISPONIBLE": {
                "texto": "Disponible",
                "fondo": "#14532D",
                "color": ft.Colors.GREEN_200,
            },
            "AGOTADO": {
                "texto": "Agotado",
                "fondo": "#7F1D1D",
                "color": ft.Colors.RED_200,
            },
            "MANTENCION": {
                "texto": "Mantención",
                "fondo": "#7C2D12",
                "color": ft.Colors.ORANGE_200,
            },
        }

        datos = configuracion.get(
            estado,
            {
                "texto": estado,
                "fondo": "#334155",
                "color": ft.Colors.GREY_200,
            },
        )

        return ft.Container(
            content=ft.Text(
                datos["texto"],
                size=12,
                weight=ft.FontWeight.BOLD,
                color=datos["color"],
            ),
            padding=ft.Padding.symmetric(
                horizontal=10,
                vertical=5,
            ),
            bgcolor=datos["fondo"],
            border_radius=20,
        )


    # ======================================================
    # MOSTRAR LIBROS EN LA TABLA
    # ======================================================

    def mostrar_libros(libros: list):
        """Coloca una lista de libros en la tabla."""

        tabla.rows.clear()
        total = len(libros)

        disponibles = sum(
            1
            for libro in libros
            if libro.get("estado") == "DISPONIBLE"
        )

        agotados = sum(
            1
            for libro in libros
            if libro.get("estado") == "AGOTADO"
        )

        mantencion = sum(
            1
            for libro in libros
            if libro.get("estado") == "MANTENCION"
        )

        txt_total.value = str(total)
        txt_disponibles.value = str(disponibles)
        txt_agotados.value = str(agotados)
        txt_mantencion.value = str(mantencion)

        for libro in libros:
            libro_actual = libro

            acciones = ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=ft.Colors.BLUE_600,
                        tooltip="Editar libro",
                        on_click=lambda e, libro=libro_actual:
                            seleccionar_libro(libro),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_600,
                        tooltip="Eliminar libro",
                        on_click=lambda e, libro=libro_actual:
                            confirmar_eliminacion(libro),
                    ),
                ],
            )

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(str(libro.get("id", "")))
                    ),
                    ft.DataCell(
                        ft.Text(str(libro.get("titulo", "")))
                    ),
                    ft.DataCell(
                        ft.Text(str(libro.get("autor", "")))
                    ),
                    ft.DataCell(
                        ft.Text(str(libro.get("genero", "")))
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(libro.get("isbn") or "Sin ISBN")
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(libro.get("anio_publicacion", ""))
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(libro.get("ejemplares", ""))
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(libro.get("ubicacion", ""))
                        )
                    ),
                    ft.DataCell(
                        crear_etiqueta_estado(
                            str(libro.get("estado", ""))
                        )
                    ),
                    ft.DataCell(acciones),
                ],
            )

            tabla.rows.append(fila)

        page.update()


    # ======================================================
    # CARGAR TODOS LOS LIBROS
    # ======================================================

    def cargar_libros(e=None):
        """Solicita todos los libros a FastAPI."""

        try:
            respuesta = requests.get(
                API_URL,
                timeout=5,
            )

            respuesta.raise_for_status()
            libros = respuesta.json()

            mostrar_libros(libros)

        except requests.ConnectionError:
            mostrar_mensaje(
                "No se puede conectar con FastAPI.",
                es_error=True,
            )

        except requests.RequestException:
            mostrar_mensaje(
                "No fue posible cargar los libros.",
                es_error=True,
            )


    # ======================================================
    # GUARDAR O ACTUALIZAR
    # ======================================================

    def guardar_libro(e):
        """Registra un libro nuevo o actualiza uno existente."""

        if not validar_formulario():
            return

        datos = obtener_datos_formulario()

        try:
            # Si no hay ID, registramos un libro.
            if libro_id_edicion is None:
                respuesta = requests.post(
                    API_URL,
                    json=datos,
                    timeout=5,
                )

                mensaje_correcto = (
                    "Libro registrado correctamente."
                )

            # Si hay un ID, actualizamos el libro seleccionado.
            else:
                respuesta = requests.put(
                    f"{API_URL}{libro_id_edicion}",
                    json=datos,
                    timeout=5,
                )

                mensaje_correcto = (
                    "Libro actualizado correctamente."
                )

            if not respuesta.ok:
                mostrar_mensaje(
                    obtener_error(respuesta),
                    es_error=True,
                )
                return

            limpiar_formulario()
            cargar_libros()

            mostrar_mensaje(mensaje_correcto)

        except requests.ConnectionError:
            mostrar_mensaje(
                "No se puede conectar con FastAPI.",
                es_error=True,
            )

        except requests.RequestException:
            mostrar_mensaje(
                "No fue posible guardar el libro.",
                es_error=True,
            )


    # ======================================================
    # SELECCIONAR UN LIBRO PARA EDITAR
    # ======================================================

    def seleccionar_libro(libro: dict):
        """Carga un libro en el formulario para editarlo."""

        nonlocal libro_id_edicion

        libro_id_edicion = libro["id"]

        txt_titulo.value = libro.get("titulo", "")
        txt_autor.value = libro.get("autor", "")
        txt_genero.value = libro.get("genero", "")
        txt_isbn.value = libro.get("isbn") or ""
        txt_anio.value = str(
            libro.get("anio_publicacion", "")
        )
        txt_ejemplares.value = str(
            libro.get("ejemplares", "")
        )
        txt_ubicacion.value = libro.get("ubicacion", "")
        dd_estado.value = libro.get(
            "estado",
            "DISPONIBLE",
        )

        btn_guardar.text = "Actualizar libro"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar.visible = True

        page.update()


    # ======================================================
    # CANCELAR LA EDICIÓN
    # ======================================================

    def cancelar_edicion(e):
        """Cancela la edición y limpia el formulario."""

        limpiar_formulario()


    # ======================================================
    # BUSCAR LIBROS
    # ======================================================

    def buscar_libros(e):
        """Busca libros por título, autor, género o ISBN."""

        texto = txt_buscar.value.strip()

        if len(texto) < 2:
            mostrar_mensaje(
                "Escribe al menos dos caracteres.",
                es_error=True,
            )
            return

        try:
            respuesta = requests.get(
                f"{API_URL}buscar/",
                params={"texto": texto},
                timeout=5,
            )

            if not respuesta.ok:
                mostrar_mensaje(
                    obtener_error(respuesta),
                    es_error=True,
                )
                return

            libros = respuesta.json()
            mostrar_libros(libros)

            if not libros:
                mostrar_mensaje(
                    "No se encontraron libros.",
                    es_error=True,
                )

        except requests.ConnectionError:
            mostrar_mensaje(
                "No se puede conectar con FastAPI.",
                es_error=True,
            )

        except requests.RequestException:
            mostrar_mensaje(
                "No fue posible realizar la búsqueda.",
                es_error=True,
            )


    # ======================================================
    # MOSTRAR TODOS
    # ======================================================

    def mostrar_todos(e):
        """Limpia el buscador y recupera todos los libros."""

        txt_buscar.value = ""
        cargar_libros()


    # ======================================================
    # CONFIRMAR ELIMINACIÓN
    # ======================================================

    def confirmar_eliminacion(libro: dict):
        """Pregunta antes de eliminar un libro."""

        def cerrar_dialogo(e):
            """Cierra el diálogo sin eliminar."""

            page.pop_dialog()

        def aceptar_eliminacion(e):
            """Cierra el diálogo y elimina el libro."""

            page.pop_dialog()
            eliminar_libro(libro["id"])

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar libro"),
            content=ft.Text(
                f'¿Deseas eliminar "{libro["titulo"]}"?'
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cerrar_dialogo,
                ),
                ft.Button(
                    "Eliminar",
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    on_click=aceptar_eliminacion,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialogo)


    # ======================================================
    # ELIMINAR LIBRO
    # ======================================================

    def eliminar_libro(libro_id: int):
        """Elimina un libro utilizando su ID."""

        try:
            respuesta = requests.delete(
                f"{API_URL}{libro_id}",
                timeout=5,
            )

            if not respuesta.ok:
                mostrar_mensaje(
                    obtener_error(respuesta),
                    es_error=True,
                )
                return

            # Si se estaba editando el libro eliminado,
            # limpiamos el formulario.
            if libro_id_edicion == libro_id:
                limpiar_formulario()

            cargar_libros()

            mostrar_mensaje(
                "Libro eliminado correctamente."
            )

        except requests.ConnectionError:
            mostrar_mensaje(
                "No se puede conectar con FastAPI.",
                es_error=True,
            )

        except requests.RequestException:
            mostrar_mensaje(
                "No fue posible eliminar el libro.",
                es_error=True,
            )


    # ======================================================
    # BOTONES
    # ======================================================

    btn_guardar = ft.Button(
        "Guardar libro",
        icon=ft.Icons.SAVE,
        on_click=guardar_libro,
        bgcolor=ft.Colors.INDIGO_600,
        color=ft.Colors.WHITE,
    )

    btn_cancelar = ft.OutlinedButton(
        "Cancelar edición",
        icon=ft.Icons.CLOSE,
        on_click=cancelar_edicion,
        visible=False,
    )

    btn_buscar = ft.Button(
        "Buscar",
        icon=ft.Icons.SEARCH,
        on_click=buscar_libros,
        bgcolor=ft.Colors.INDIGO_600,
        color=ft.Colors.WHITE,
    )

    btn_mostrar_todos = ft.OutlinedButton(
        "Mostrar todos",
        icon=ft.Icons.REFRESH,
        on_click=mostrar_todos,
    )


    # ======================================================
    # ORGANIZACIÓN DEL FORMULARIO
    # ======================================================

    formulario = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    txt_titulo,
                    txt_autor,
                ],
            ),
            ft.Row(
                controls=[
                    txt_genero,
                    txt_isbn,
                ],
            ),
            ft.Row(
                controls=[
                    txt_anio,
                    txt_ejemplares,
                    txt_ubicacion,
                    dd_estado,
                ],
            ),
        ],
    )

    page.add(
        # ==================================================
        # ENCABEZADO
        # ==================================================

        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.LOCAL_LIBRARY,
                            size=38,
                            color=ft.Colors.WHITE,
                        ),
                        padding=12,
                        bgcolor="#4F46E5",
                        border_radius=14,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Biblioteca Escolar",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "Administración del catálogo de libros",
                                size=14,
                                color=ft.Colors.GREY_300,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
            ),
            padding=ft.Padding.symmetric(
                horizontal=30,
                vertical=24,
            ),
            bgcolor="#111827",
        ),

        # ==================================================
        # CONTENIDO PRINCIPAL
        # ==================================================

        ft.Container(
            content=ft.Column(
                controls=[
                    # Indicadores.
                    ft.Row(
                        controls=[
                            tarjeta_total,
                            tarjeta_disponibles,
                            tarjeta_agotados,
                            tarjeta_mantencion,
                        ],
                    ),

                    # Formulario.
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.EDIT_NOTE,
                                            color=ft.Colors.INDIGO_300,
                                        ),
                                        ft.Text(
                                            "Información del libro",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                                ft.Divider(),
                                formulario,
                                ft.Row(
                                    controls=[
                                        btn_cancelar,
                                        btn_guardar,
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                        ),
                        padding=22,
                        bgcolor="#1E293B",
                        border_radius=16,
                    ),

                    # Catálogo.
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.MENU_BOOK,
                                            color=ft.Colors.INDIGO_300,
                                        ),
                                        ft.Text(
                                            "Catálogo de libros",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                                ft.Divider(),
                                ft.Row(
                                    controls=[
                                        txt_buscar,
                                        btn_buscar,
                                        btn_mostrar_todos,
                                    ],
                                ),
                                ft.Row(
                                    controls=[tabla],
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                            ],
                        ),
                        padding=22,
                        bgcolor="#1E293B",
                        border_radius=16,
                    ),
                ],
                spacing=20,
            ),
            padding=30,
        ),
    )


    # Carga inicial de los libros.
    cargar_libros()


if __name__ == "__main__":
    ft.run(main)