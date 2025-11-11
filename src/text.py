import flet as ft


def item_title(text: str, size: ft.Number = 52):
    return ft.Text(text, font_family="Lobster", size=size, color="#5C412A")

def checkout_text(text: str, weight: ft.FontWeight):
    return ft.Text(value=text, weight=weight, font_family="Inter", size=32)