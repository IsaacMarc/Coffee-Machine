import flet as ft
import asyncio
from menu import Menu
from coffee_maker import CoffeeMaker
from setup import fix_stretched_window
from components import (preset_appbar, exit_button, minimize_button, item_content, loading_screen_container,
                        item_container, brewing_coffee_title_container, skip_button, default_title_container,
                        default_data_cell, default_data_column)
from notifications import simple_notification, simple_dialog
from images import money_img
from text import checkout_text, pomc_text_comp
from utilities import skippable_delay
from layouts import default_row


async def main_ui(page: ft.Page):
    # == Initial Setup ==
    # Loading Screen
    page.add(loading_screen_container())
    await fix_stretched_window(page, center_page=True)
    
    # Variables
    choice: str = ""
    payment: int = 0
    cost: int = 125
    menu_coffee = Menu()
    coffee = CoffeeMaker()
    purchase_history_rows: list[ft.DataRow] = []
    
    # == UI Setup ==
    # Event Handlers
    def on_payment(_):
        nonlocal payment
        drink = menu_coffee.find_drink(choice)
        if coffee.is_resource_sufficient(drink) and drink and payment >= cost:
            coffee.make_coffee(drink)
        if payment >= cost:
            msg = "Payment Successful! Recieved Exact Cash." if payment == cost else "Payment Successful!"
            simple_notification(msg, page)
            order_num = len(purchase_history_rows) + 1
            print(f"Received Order Number: {order_num}")
            purchase_history_rows.append(
                ft.DataRow(cells=[
                    default_data_cell(order_num),
                    default_data_cell(choice.capitalize()),
                    default_data_cell(f"₱{cost}"),
                    default_data_cell(f"₱{payment}"),
                    default_data_cell(f"₱{payment - cost}")
                ])
            )
            print(f"Purchase history is now {len(purchase_history_rows)} entries long.")
            payment = 0
            asyncio.create_task(brew_coffee())
        else:
            simple_notification(f"Insufficient Funds! Missing ₱{cost - payment}", page, is_error=True)
    
    def on_confirm(_):
        form.content = post_order_menu_bg
        form.update()
        close_dlg()
    
    def on_dismiss(_):
        nonlocal choice
        choice = ""
        close_dlg()
    
    def on_click_lat(_):
        nonlocal choice
        choice = "latte"
        open_confirmation_dlg()
    
    def on_click_cap(_):
        nonlocal choice
        choice = "cappuccino"
        open_confirmation_dlg()
    
    def on_click_esp(_):
        nonlocal choice
        choice = "espresso"
        open_confirmation_dlg()
    
    def open_purchase_history(_):
        if not purchase_history_rows:
            nonlocal notif_dlg
            notif_dlg.open = True
            page.update()
            return
        
        page.overlay.pop(1)
        notif_dlg = simple_dialog("Purchase History", ft.Icons.HISTORY, "Empty")
        notif_dlg.content = purchase_history_table
        page.overlay.append(notif_dlg)
        notif_dlg.open = True
        page.update()
    
    # Events
    async def brew_coffee():
        await asyncio.sleep(1.5)
        skip_event = asyncio.Event()
        skip_event.clear()
        skip_btn = skip_button(skip_event)
        
        new_container = default_title_container(brewing_coffee_title_container(skip_btn))
        form.content = new_container
        form.update()
        update_texts()
        await skippable_delay(skip_event, 16, clear_after_skip=True)
        
        form.content = ft.Stack(
            controls=[
                ft.Container(
                    ft.Image(
                        src="images/coffee_dispense.gif", 
                        expand=True, fit=ft.BoxFit.CONTAIN
                    ), expand=True, alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    content=skip_btn, padding=8,
                    alignment=ft.Alignment.BOTTOM_CENTER
                ),
                ft.Container(
                    ft.Text(
                        value=f"Dispensing: {choice.capitalize()}", size=28,
                        font_family="Lobster", color="#38220F",
                        text_align=ft.TextAlign.CENTER
                    ), bgcolor=ft.Colors.WHITE,
                    border_radius=30, left=60, top=10, padding=8
                )
            ],
            expand=True
        )
        form.update()
        await skippable_delay(skip_event, 17, clear_after_skip=True)
        
        form.content = default_title_container(
            ft.Text(
                value=f"Enjoy your {choice.capitalize()}!", size=64,
                color=ft.Colors.WHITE, weight=ft.FontWeight.W_800
            ),
            on_click=lambda _: skip_event.set()
        )
        form.update()
        await skippable_delay(skip_event, 5, clear_after_skip=True)
        
        form.content = bg_container
        form.update()
    
    # Post-Order Menu Container
    pomc_text = ft.Column(controls=[
        checkout_text("ORDER AMOUNT", ft.FontWeight.W_800),
        ft.Divider(ft.Colors.BLACK),
        pomc_text_comp("Total Amount: ₱", 125),
        pomc_text_comp("Amount Tendered: ₱"),
        pomc_text_comp("Change: ₱"),
        ft.Button(
            content=ft.Text("Pay", color=ft.Colors.WHITE, size=30),
            elevation=10, width=200, bgcolor="#5C412A",
            on_click=on_payment
        )
    ])
    
    def update_texts():
        payment_text: ft.Text = pomc_text.controls[3]
        change_text: ft.Text = pomc_text.controls[4]
        payment_text.spans[1].text = payment
        if payment >= cost:
            change_text.spans[1].text = payment - cost
        else:
            change_text.spans[1].text = 0
        pomc_text.update()
    
    def open_confirmation_dlg():
        confirmation_dlg.open = True
        page.update()
    
    def close_dlg():
        confirmation_dlg.open = False
        page.update()
    
    # Components
    purchase_history_table = ft.DataTable(
        columns=[
            default_data_column("No."),
            default_data_column("Order"),
            default_data_column("Total"),
            default_data_column("Cash Tendered"),
            default_data_column("Change")
        ], rows=purchase_history_rows
    )
    
    notif_dlg = simple_dialog("Purchase History", ft.Icons.HISTORY, "Empty")
    
    purchase_history_btn = ft.Button(
        content=ft.Text("Show Purchase History", color="#38220F"),
        icon=ft.Icons.HISTORY, icon_color="#38220F",
        on_click=open_purchase_history
    )
    
    appbar = preset_appbar([
        purchase_history_btn, ft.Container(width=50),
        minimize_button(page), exit_button(page)
    ])
    
    latte_container = item_content("Latte")
    espresso_container = item_content("Espresso")
    cappuccino_container = item_content("Cappuccino")
    
    def money_container(value: int):
        async def on_click(_):
            nonlocal payment
            payment += value
            update_texts()
            ctrl.opacity = 0.7
            ctrl.scale = 0.9
            ctrl.update()
            await asyncio.sleep(0.2)
            ctrl.opacity = 1
            ctrl.scale = 1
            ctrl.update()
        
        def on_hover(e: ft.ControlEvent):
            if e.data == True:
                ctrl.offset = ft.Offset(0.0, -0.2)
                ctrl.update()
            else:
                ctrl.offset = ft.Offset(0.0, 0.0)
                ctrl.update()
        
        ctrl = ft.Container(
            content=money_img(value), offset=ft.Offset(0.0, 0.0),
            animate_offset=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=on_hover, on_click=on_click
        )
        return ctrl
    
    money_row = ft.Stack(
        controls=[
            money_container(1),
            money_container(5),
            money_container(10),
            money_container(20),
            money_container(50),
            money_container(100),
            money_container(500),
            money_container(1000)
        ], alignment=ft.Alignment.BOTTOM_CENTER
    )
    
    for i in range(len(money_row.controls)):
        money: ft.Image = money_row.controls[i]
        money.left = i * 100
        if i >= 4:
            money.left += 100
    
    post_order_menu_content = ft.Stack(   
        controls=[
            pomc_text, money_row
        ], alignment=ft.Alignment.BOTTOM_CENTER
    )
    
    post_order_menu_bg = ft.Container(
        padding=16,
        content=post_order_menu_content,
        alignment=ft.Alignment.CENTER,
        bgcolor="#ECE0D1",
        border_radius=31, margin=16,
        width=1167, height=610
    )
    
    confirmation_dlg = ft.AlertDialog(
        title=ft.Text("Confirm Order?", size=32, weight=ft.FontWeight.W_800),
        actions=[
            ft.Button(ft.Text("Yes", size=20), on_click=on_confirm),
            ft.Button(ft.Text("No", size=20), on_click=on_dismiss)
        ], open=False, modal=True,
        actions_alignment=ft.MainAxisAlignment.CENTER
    )
    
    item_row = default_row([
        item_container(latte_container, width=381, on_click=on_click_lat),
        item_container(cappuccino_container, width=369, on_click=on_click_cap),
        item_container(espresso_container, width=322, on_click=on_click_esp)
    ])
    
    bg_container = ft.Container(
        padding=16, content=item_row,
        alignment=ft.Alignment.CENTER,
        bgcolor="#ECE0D1",
        border_radius=63, margin=16,
        width=1167, height=610
    )
    
    form = ft.WindowDragArea(
        content=bg_container, maximizable=False,
        expand=True
    )
    
    # Page Stuff
    page.appbar = appbar
    page.controls.clear()
    page.add(form)
    page.overlay.extend([confirmation_dlg, notif_dlg])
    