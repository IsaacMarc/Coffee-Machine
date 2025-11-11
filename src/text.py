import flet as ft


def item_title(text: str, size: ft.Number = 52):
    return ft.Text(text, font_family="Lobster", size=size, color="#5C412A")

def checkout_text(text: str, weight: ft.FontWeight):
    return ft.Text(value=text, weight=weight, size=32)

def pomc_text_comp(text: str, value: int = 0) -> ft.Text:
    return ft.Text(
        spans=[
            ft.TextSpan(text),
            ft.TextSpan(value)
        ], size=32, weight=ft.FontWeight.W_600
    )