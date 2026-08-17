import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/libros/"

def main(page: ft.Page):

    page.title = "Biblioteca Escolar"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    txt_titulo = ft.TextField(label="Titulo")
    txt_autor = ft.TextField(label="Autor")
    txt_genero = ft.TextField(label="Genero")
    txt_anio = ft.TextField(label="Año de Publicacion")
    txt_ejemplares = ft.TextField(label="Numero de Ejemplares")
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Titulo")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Genero")),
            ft.DataColumn(ft.Text("Año de Publicacion")),
            ft.DataColumn(ft.Text("Numero de Ejemplares")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[],
    )

    formulario = ft.Column(
        controls=[
            txt_titulo,
            txt_autor,
            txt_genero,
            txt_anio,
            txt_ejemplares,
        ]
    )

    def cargar_libros():
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            libros = respuesta.json()
            tabla.rows.clear()    

            for libro in libros:
                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(libro.get("id", "")))),
                        ft.DataCell(ft.Text(str(libro.get("titulo", "")))),
                        ft.DataCell(ft.Text(str(libro.get("autor", "")))),
                        ft.DataCell(ft.Text(str(libro.get("genero", "")))),
                        ft.DataCell(ft.Text(str(libro.get("anio_publicacion", "")))),
                        ft.DataCell(ft.Text(str(libro.get("ejemplares", "")))),
                        ft.DataCell(ft.Text("Acciones")),
                    ]
                )
                tabla.rows.append(fila)
            page.update()

        except requests.ConnectionError:
            print("No se puede conectar!!!!")
           
            
    page.add(
        ft.Text("Biblioteca Escolar", size=30, weight=ft.FontWeight.BOLD),
        formulario,
        tabla,        
    )
    cargar_libros()

if __name__ == "__main__":
    ft.run(main)