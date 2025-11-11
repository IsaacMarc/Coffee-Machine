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

def simple_popup_menu_item(
    text: str,
    color: ft.ColorValue,
    icon: ft.IconData,
    on_click: Optional[ft.ControlEventHandler[ft.PopupMenuItem]] = None,
    checked: Optional[bool] = None
) -> ft.PopupMenuItem:
    """A popup menu item that handles self-toggling if needed."""
    def default_on_click(e: ft.ControlEventHandler[ft.PopupMenuItem]):
        """`e` only has `name="click"` and `data: bool`"""
        popup_menu_item.checked = e.data
        popup_menu_item.update()
    if checked is not None and on_click is None:
        on_click=default_on_click
    popup_menu_item = ft.PopupMenuItem(
        content=ft.Text(value=text, color=color),
        icon=ft.Icon(icon=icon, color=color),
        on_click=on_click, checked=checked
    )
    return popup_menu_item

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

def preset_popup_menu_button(
    menu_items: list[ft.PopupMenuItem]
) -> ft.PopupMenuButton:
    """An extensive popup menu button, that serves as an extra options menu."""
    async def on_open(e: ft.ControlEvent):
        await asyncio.sleep(0.5)
        popup_menu_btn: ft.PopupMenuButton = e.control
        popup_menu_btn.badge = None
        await asyncio.sleep(0.5)
        popup_menu_btn.update()
    
    return ft.PopupMenuButton(
        items=[*menu_items], icon_color="#38220F",
        badge=ft.Badge(small_size=10), on_open=on_open
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