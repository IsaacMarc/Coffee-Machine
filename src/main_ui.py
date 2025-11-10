import flet as ft
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
from setup import fix_stretched_window
from components import preset_appbar, exit_button, minimize_button


def item_container(text: str, width: ft.Number, height: ft.Number):
    return ft.Container(
        content=ft.Text(text),
        padding=8, alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        border_radius=63,
        width=width, height=height
    )



async def main_ui(page: ft.Page):
    await fix_stretched_window(page, center_page=True)
    
    # Components
    appbar = preset_appbar([
        minimize_button(page), exit_button(page)
    ])
    
    item_row = ft.Row(
        controls=[
            item_container("Latte", 381, 577),
            item_container("Espresso", 322, 577),
            item_container("Cappuccino", 369, 577)
        ], spacing=16, expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=16, run_alignment=ft.MainAxisAlignment.CENTER
    )
    
    bg_container = ft.Container(
        padding=16, content=item_row,
        alignment=ft.Alignment.CENTER,
        bgcolor="#ECE0D1",
        border_radius=63, margin=16,
        width=1167, height=610
    )
    
    # Page Stuff
    page.appbar = appbar
    page.add(bg_container)
    