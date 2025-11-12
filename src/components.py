import flet as ft
import asyncio
from typing import Optional
from layouts import default_column
from text import item_title
from images import coffee_img


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

def skip_button(skip_event: asyncio.Event):
    return ft.Button(
        content=ft.Text("Skip", size=20, weight=ft.FontWeight.W_400),
        on_click=lambda _: skip_event.set(), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
        elevation=10, width=100
    )

# App Bar
def preset_appbar(actions: list[ft.Control]) -> ft.AppBar:
    """A simple predefined appbar."""
    return ft.AppBar(
        leading=ft.WindowDragArea(
            ft.Container(
                ft.Image(src="icon.png", fit=ft.BoxFit.CONTAIN, expand=True),
                padding=8
            ),
            maximizable=False, expand=True
        ),
        title=ft.WindowDragArea(
            content=ft.Text("Fletto 'Spresso Machine", color="#5C412A"),
            maximizable=False, expand=True
        ),
        actions=actions, bgcolor=ft.Colors.WHITE,
        actions_padding=4, title_spacing=4,
        shape=ft.RoundedRectangleBorder(radius=5)
    )
    
# Containers
def item_subcontent(on_click: ft.ControlEvent):
    return ft.Column(
        controls=[
            ft.Text("₱125.00",size=24, weight=ft.FontWeight.W_600, color="#453426"),
            ft.Button(
                ft.Text("Ingredients", font_family="Lobster", size=20, color=ft.Colors.WHITE),
                width=142, height=36, bgcolor="#967259", elevation=10, on_click=on_click
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
def loading_screen_container():
    return default_column([
        item_title("Starting Up the Coffee Machine...", size=35),
        ft.ProgressRing(width=150, height=150, color="#453426", padding=8)
    ])

def item_container(
    content: ft.StrOrControl, *, width: ft.Number, height: ft.Number = 577,
    on_click: ft.ControlEventHandler[ft.Container]
):
    def on_hover(e: ft.ControlEvent):
        if e.data:
            container.bgcolor = ft.Colors.WHITE
        else:
            container.bgcolor = ft.Colors.TRANSPARENT
        container.update()
    
    container = ft.Container(
        content=content,
        padding=8, alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=63,
        width=width, height=height,
        on_hover=on_hover,
        on_click=on_click
    )
    return container

def item_content(title: str):
    async def on_click(_):
        stack.controls.append(hover_content)
        stack.update()
        await asyncio.sleep(0.1)
        hover_content.opacity = 1
        hover_content.update()
        await asyncio.sleep(3)
        hover_content.opacity = 0
        hover_content.update()
        await asyncio.sleep(1)
        stack.controls.remove(hover_content)
        stack.update()
        
    main_content = ft.Column(
        controls=[
            coffee_img(title.lower()),
            item_title(title),
            item_subcontent(on_click)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    values = {
        "Espresso": "a strong, concentrated coffee shot with crema.",
        "Latte": "espresso, steamed milk, and a thin layer of frothed milk.",
        "Cappuccino": "espresso, steamed milk, and a thick layer of frothed milk."
    }
    hover_content = ft.Container(
        content=ft.Text(
            value=values[title],
            font_family="Libre Caslon", size=40, color=ft.Colors.WHITE
        ), border_radius=63, width=381, height=577,
        bgcolor=ft.Colors.with_opacity(0.79, ft.Colors.BLACK),
        alignment=ft.Alignment.CENTER, padding=16, opacity=0,
        animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT)
    )
    stack = ft.Stack(
        controls=[
            main_content
        ], alignment=ft.Alignment.CENTER
    )
    return stack

def brewing_coffee_title_container(skip_button: ft.Button):
    return default_column([
        ft.Text(
            value="Your Coffee is Brewing", size=64,
            color=ft.Colors.WHITE, weight=ft.FontWeight.W_800
        ),
        ft.ProgressRing(width=150, height=150, color=ft.Colors.WHITE, padding=16),
        skip_button
    ])

def default_title_container(
    content: ft.Control, *,
    on_click: ft.ControlEventHandler[ft.Container] | None = None
):
    return ft.Container(
        content=content, bgcolor="#38220F", expand=True,
        alignment=ft.Alignment.CENTER, on_click=on_click
    )

def default_data_cell(text: str) -> ft.DataCell:
    return ft.DataCell(
        content=ft.Text(value=text, size=15)
    )

def default_data_column(text: str) -> ft.DataColumn:
    return ft.DataColumn(
        tooltip=text, label=ft.Text(
            value=text, size=25,
            weight=ft.FontWeight.W_700
        )
    )