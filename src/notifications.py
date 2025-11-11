import flet as ft


def simple_notification(
    content: str, page: ft.Page, duration: int = 2000,
    *, is_error: bool = False
):
    snackbar = ft.SnackBar(
        content=ft.Text(value=content, size=20, font_family="Inter"), open=True,
        duration=duration, behavior=ft.SnackBarBehavior.FLOATING,
        on_dismiss=lambda e: page.overlay.remove(e.control),
        bgcolor="#5C412A"
    )
    if is_error:
        text: ft.Text = snackbar.content
        text.color = ft.Colors.ERROR
        snackbar.bgcolor = ft.Colors.ERROR_CONTAINER
    page.overlay.append(snackbar)

def simple_dialog(
    title: str, icon: ft.IconData, content: str, *,
    title_size: ft.Number = 30
):
    return ft.AlertDialog(
        title=ft.Text(value=title, color="#38220F", font_family="Lobster", size=title_size),
        icon=ft.Icon(icon=icon, size=title_size),
        icon_color="#38220F",
        content=ft.Text(value=content, color="#38220F", font_family="Inter", size=title_size-10),
        bgcolor=ft.Colors.WHITE, elevation=10, open=False, scrollable=True
    )