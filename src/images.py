import flet as ft


def coffee_img(coffee_type: str):
    return ft.Image(
        src=f"images/coffee/{coffee_type}.png", fit=ft.BoxFit.CONTAIN,
        width=342, height=342, offset=ft.Offset(0.0, 0.1)
    )

def money_img(value: int):
    src = f"images/money/{value}.png"
    return ft.Image(src=src, fit=ft.BoxFit.CONTAIN)