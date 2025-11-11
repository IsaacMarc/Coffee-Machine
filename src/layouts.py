import flet as ft


def default_column(controls: list[ft.Control]) -> ft.Column:
    return ft.Column(
        controls=controls, alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )