import flet as ft
import asyncio
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
from setup import fix_stretched_window
from components import (preset_appbar, exit_button, minimize_button,
                        preset_popup_menu_button, simple_popup_menu_item)
from notifications import simple_notification, simple_dialog


def item_container(
    content: ft.StrOrControl, *, width: ft.Number, height: ft.Number,
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

def item_title(text: str, size: ft.Number = 52):
    return ft.Text(text, font_family="Lobster", size=size, color="#5C412A")

def item_subcontent(on_click: ft.ControlEvent):
    return ft.Column(
        controls=[
            ft.Text("₱125.00", font_family="Inter", size=24, weight=ft.FontWeight.W_600, color="#453426"),
            ft.Button(
                ft.Text("Ingredients", font_family="Lobster", size=20, color=ft.Colors.WHITE),
                width=142, height=36, bgcolor="#967259", elevation=10, on_click=on_click
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def coffee_img(coffee_type: str):
    return ft.Image(
        src=f"images/coffee/{coffee_type}.png", fit=ft.BoxFit.CONTAIN,
        width=342, height=342, offset=ft.Offset(0.0, 0.1)
    )

def money_img(value: int):
    src = f"images/money/{value}.png"
    return ft.Image(src=src, fit=ft.BoxFit.CONTAIN)

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

def checkout_text(text: str, weight: ft.FontWeight):
    return ft.Text(value=text, weight=weight, font_family="Inter", size=32)

async def main_ui(page: ft.Page):
    # == Initial Setup ==
    # Loading Screen
    page.add(
        ft.Column(
            controls=[
                item_title("Starting Up the Coffee Machine...", size=25),
                ft.ProgressRing(width=100, height=100)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    await fix_stretched_window(page, center_page=True)
    
    # Variables
    choice: str = ""
    payment: int = 0
    cost: int = 125
    menu_coffee = Menu()
    coffee = CoffeeMaker()
    money = MoneyMachine()
    purchase_history: list[ft.TextSpan] = []
    
    # == UI Setup ==
    # Event Handlers
    def on_payment(_):
        nonlocal payment
        drink = menu_coffee.find_drink(choice)
        if coffee.is_resource_sufficient(drink) and drink and payment >= cost:
            coffee.make_coffee(drink)
        if payment >= cost:
            msg = "Payment Successful: Recieved Exact Cash" if payment == cost else "Payment Successful"
            simple_notification(msg, page)
            new_entry = ft.TextSpan("Temp")
            purchase_history.append(new_entry)
            new_entry.text = f"Order #{len(purchase_history)}: {choice} | Total: {cost} | Cash Tendered: {payment} | Change: {payment - cost}\n"
            print(f"Purchase history is now {len(purchase_history)} entries long.")
            payment = 0
            asyncio.create_task(brew_coffee())
        else:
            simple_notification("Insufficient Funds!", page, is_error=True)
    
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
        if not purchase_history:
            nonlocal notif_dlg
            notif_dlg.open = True
            page.update()
            return
        
        page.overlay.pop(1)
        notif_dlg = simple_dialog("Purchase History", ft.Icons.HISTORY, "Empty")
        text: ft.Text = notif_dlg.content
        text.value = ""
        text.spans = purchase_history
        page.overlay.append(notif_dlg)
        notif_dlg.open = True
        page.update()
    
    # Events
    async def brew_coffee():
        await asyncio.sleep(1.5)
        skip_event = asyncio.Event()
        skip_event.clear()
        skip_button = ft.Button(
            content=ft.Text("Skip", size=20, font_family="Inter", weight=ft.FontWeight.W_400),
            on_click=lambda _: skip_event.set(), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
            elevation=10, width=100
        )
        
        new_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Your Coffee is Brewing", font_family="Inter",
                        size=64, color=ft.Colors.WHITE, weight=ft.FontWeight.W_800
                    ),
                    ft.ProgressRing(width=100, height=100),
                    skip_button
                ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#38220F", expand=True, alignment=ft.Alignment.CENTER
        )
        form.content = new_container
        form.update()
        update_texts()
        try:
            await asyncio.wait_for(skip_event.wait(), timeout=16)
            print("Wait skipped!")
        except asyncio.TimeoutError:
            print("Wait finished naturally.")
        skip_event.clear()
            
        form.content = ft.Stack(
            controls=[
                ft.Container(
                    ft.Image(
                        src="images/coffee_dispense.gif", 
                        expand=True, fit=ft.BoxFit.CONTAIN
                    ), expand=True, alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    content=skip_button, padding=8,
                    alignment=ft.Alignment.BOTTOM_CENTER
                ),
                ft.Container(
                    ft.Text(
                        value=f"Dispensing: {choice}", size=28,
                        font_family="Lobster", color="#38220F",
                        text_align=ft.TextAlign.CENTER
                    ), bgcolor=ft.Colors.WHITE,
                    border_radius=30, left=60, top=10, padding=8
                )
            ],
            expand=True
        )
        form.update()
        try:
            await asyncio.wait_for(skip_event.wait(), timeout=16)
            print("Wait skipped!")
        except asyncio.TimeoutError:
            print("Wait finished naturally.")
        skip_event.clear()
        
        form.content = ft.Container(
            ft.Text(
                value=f"Enjoy your {choice}!", font_family="Inter",
                size=64, color=ft.Colors.WHITE, weight=ft.FontWeight.W_800
            ), bgcolor="#38220F", expand=True, alignment=ft.Alignment.CENTER,
            on_click=lambda _: skip_event.set()
        )
        form.update()
        try:
            await asyncio.wait_for(skip_event.wait(), timeout=5)
            print("Wait skipped!")
        except asyncio.TimeoutError:
            print("Wait finished naturally.")
        
        form.content = bg_container
        form.update()
       
    pomc_text = ft.Column(controls=[
        checkout_text("ORDER AMOUNT", ft.FontWeight.W_800),
        ft.Divider(ft.Colors.BLACK),
        ft.Text(
            spans=[
                ft.TextSpan("Total Amount: ₱"),
                ft.TextSpan(125)
            ], font_family="Inter", size=32, weight=ft.FontWeight.W_600
        ),
        ft.Text(
            spans=[
                ft.TextSpan("Amount Tendered: ₱"),
                ft.TextSpan(0)
            ], font_family="Inter", size=32, weight=ft.FontWeight.W_600
        ),
        ft.Text(
            spans=[
                ft.TextSpan("Change: ₱"),
                ft.TextSpan(0)
            ], font_family="Inter", size=32, weight=ft.FontWeight.W_600
        ),
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
    notif_dlg = simple_dialog("Purchase History", ft.Icons.HISTORY, "Empty")
    
    popup_menu = preset_popup_menu_button([
        simple_popup_menu_item(
            text="Show Purchase History", color="#38220F",
            icon=ft.Icons.HISTORY, on_click=open_purchase_history
        )
    ])
    
    appbar = preset_appbar([
        popup_menu, ft.Container(width=50),
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
        title=ft.Text(
            "Confirm Order?", font_family="Inter",
            size=32, weight=ft.FontWeight.W_800
        ), actions=[
            ft.Button(ft.Text("Yes", size=20, font_family="Inter"), on_click=on_confirm),
            ft.Button(ft.Text("No", size=20, font_family="Inter"), on_click=on_dismiss)
        ], open=False, modal=True,
        actions_alignment=ft.MainAxisAlignment.CENTER
    )
    
    item_row = ft.Row(
        controls=[
            item_container(latte_container, width=381, height=577, on_click=on_click_lat),
            item_container(cappuccino_container, width=369, height=577, on_click=on_click_cap),
            item_container(espresso_container, width=322, height=577, on_click=on_click_esp),
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
    
    form = ft.WindowDragArea(
        content=bg_container, maximizable=False,
        expand=True
    )
    
    # Page Stuff
    page.appbar = appbar
    page.controls.clear()
    page.add(form)
    page.overlay.extend([confirmation_dlg, notif_dlg])
    