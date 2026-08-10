import flet as ft

import requests
#Direccion del endpoint de libros
API_URL = "http://127.0.0.1:8000/libros/"

def main(page: ft.Page):

    #Configuracion de la pagina
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
        rows=[]
    )

