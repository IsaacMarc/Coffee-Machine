import flet as ft
import asyncio
from typing import Optional


# == Presets ==
def simple_icon_button(
    icon: ft.IconDataOrControl,
    icon_color: ft.ColorValue = ft.Colors.PRIMARY,
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.IconButton:
    """Literally just an icon button."""
    return ft.IconButton(
        icon=icon, icon_color=icon_color, on_click=on_click
    )

# == Pre-Assembled Components ==
# Buttons
def minimize_button(page: ft.Page) -> ft.IconButton:
    """Handles the window minimizing function."""
    def on_click(_):
        page.window.minimized = True
    return simple_icon_button(
        icon=ft.Icons.MINIMIZE, icon_color="#5C412A",
        on_click=on_click
    )

def exit_button(page: ft.Page) -> ft.IconButton:
    """Handles the app exit function."""
    return simple_icon_button(
        icon=ft.Icons.CLOSE, icon_color="#5C412A",
        on_click=lambda _: asyncio.create_task(
            coro=page.window.close(),
            name="Exit Button -> Closing Window"
        )
    )

# App Bar
def preset_appbar(actions: list[ft.Control]) -> ft.AppBar:
    """A simple predefined appbar."""
    return ft.AppBar(
        title=ft.WindowDragArea(
            content=ft.Text("Fletto 'Spresso Machine", color="#5C412A"),
            maximizable=False
        ),
        actions=actions,
        bgcolor=ft.Colors.WHITE,
        actions_padding=4, title_spacing=4,
        shape=ft.RoundedRectangleBorder(radius=5),
        leading_width=8, leading=ft.Container()
    )