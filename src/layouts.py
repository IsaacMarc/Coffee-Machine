import flet as ft


def default_column(controls: list[ft.Control]) -> ft.Column:
    return ft.Column(
        controls=controls, alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def default_row(controls: list[ft.Control]) -> ft.Row:
    return ft.Row(
        controls=controls, spacing=16, expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=16, run_alignment=ft.MainAxisAlignment.CENTER
    )
    