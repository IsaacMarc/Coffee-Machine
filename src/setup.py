import flet as ft


def before_main_ui(page: ft.Page):
    page.title = "Classic Cafe Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    page.window.width = 600
    page.window.height = 500
    