import flet as ft
# Assuming these files exist and contain your business logic classes
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

# --- Global Initialization (Core Logic) ---
menu_coffee = Menu()
coffee = CoffeeMaker()
money = MoneyMachine()


# --- CAFE COLOR PALETTES ---
class CafeColors:
    # Shared Colors
    MOCHA = "#8C6A5A"
    OFF_WHITE = "#FFF8DC"

    # Dark Mode
    DARK_BG = "#33221C"
    DARK_FRAME = "#4A332C"
    LATTE = "#EDE0D4"

    # Light Mode
    CREME_BG = OFF_WHITE
    LIGHT_FRAME = "#FAF0C0"

    THEMES = {
        "Dark": {
            "window_bg": DARK_BG, "frame_bg": DARK_FRAME, "header_bg": LATTE,
            "text": LATTE, "header_text": DARK_FRAME, "status_text": LATTE,
            "drink_fg": LATTE, "drink_text": DARK_FRAME, "drink_hover": MOCHA,
            "control_fg": MOCHA, "control_hover": "#7A594B", "control_text": OFF_WHITE,
            "error_fg": "#A3432F"
        },
        "Light": {
            "window_bg": CREME_BG, "frame_bg": LIGHT_FRAME, "header_bg": LATTE,
            "text": DARK_FRAME, "header_text": DARK_FRAME, "status_text": DARK_FRAME,
            "drink_fg": LATTE, "drink_text": DARK_FRAME, "drink_hover": MOCHA,
            "control_fg": MOCHA, "control_hover": "#7A594B", "control_text": OFF_WHITE,
            "error_fg": "#A3432F"
        }
    }


# --- Flet Application Class ---
class CoffeeMachineApp(ft.Control):
    # Required for custom controls inheriting from ft.Control
    def_control_name = "coffeemachineapp"

    def __init__(self):
        super().__init__()
        self.current_theme = "Dark"
        self.status_text = ft.Text("Welcome to The Classic Cafe. Order up!", size=12, italic=True)
        self.themed_widgets = {}

    def build(self):
        """Initializes widgets and returns the main layout container."""
        self._setup_widgets()
        self._apply_theme(self.current_theme)

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.themed_widgets["header_frame"],
                    self.themed_widgets["main_frame"],
                    ft.Container(height=5),  # Spacer
                    self.themed_widgets["status_bar"],
                ],
                spacing=0
            ),
            padding=ft.padding.only(top=10, bottom=10),
            expand=True
        )

    # --- Widget Setup ---
    def _setup_widgets(self):
        # 1. Header and Theme Switcher
        theme_switch = ft.Switch(
            label="Light/Dark",
            on_change=self.toggle_theme,
            value=True
        )
        header_label = ft.Text("☕ Classic Cafe Menu", size=24, weight=ft.FontWeight.BOLD)
        self.themed_widgets["header_label"] = header_label

        header_frame_row = ft.Row(
            controls=[header_label, theme_switch],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.themed_widgets["header_frame"] = ft.Container(
            content=header_frame_row,
            padding=ft.padding.all(15),
            border_radius=10
        )

        # 2. Drink Buttons Frame
        self.themed_widgets["drinks_label"] = ft.Text("Place Your Order", size=14, weight=ft.FontWeight.BOLD)
        self.themed_widgets["drink_buttons"] = []
        drink_controls = [self.themed_widgets["drinks_label"]]

        for item in menu_coffee.menu:
            # FIX: Used ft.alignment.center for consistency with the last bug fix
            btn = ft.Container(
                content=ft.Text(f"{item.name.title()} | ${item.cost:.2f}", size=16, weight=ft.FontWeight.BOLD),
                on_click=lambda e, name=item.name: self.show_payment_window(name),
                padding=15,
                alignment=ft.alignment.center,
                border_radius=8,
            )
            drink_controls.append(btn)
            self.themed_widgets["drink_buttons"].append(btn)

        drinks_frame = ft.Container(
            content=ft.Column(controls=drink_controls, spacing=8),
            padding=15,
            border_radius=10,
            expand=True
        )
        self.themed_widgets["drinks_frame"] = drinks_frame

        # 3. Control Buttons Frame
        self.themed_widgets["controls_label"] = ft.Text("Management", size=14, weight=ft.FontWeight.BOLD)

        report_btn = ft.Container(
            content=ft.Text("View Report 📊", size=14, weight=ft.FontWeight.BOLD),
            on_click=self.show_report,
            padding=15,
            alignment=ft.alignment.center,
            border_radius=8,
        )
        self.themed_widgets["report_btn"] = report_btn

        off_btn = ft.Container(
            content=ft.Text("Close Shop 🛑", size=14, weight=ft.FontWeight.BOLD),
            on_click=lambda e: self.page.window_close(),
            padding=15,
            alignment=ft.alignment.center,
            border_radius=8,
        )
        self.themed_widgets["off_btn"] = off_btn

        controls_frame = ft.Container(
            content=ft.Column(
                controls=[
                    self.themed_widgets["controls_label"],
                    report_btn,
                    off_btn
                ],
                spacing=8
            ),
            padding=15,
            border_radius=10,
            expand=True
        )
        self.themed_widgets["controls_frame"] = controls_frame

        # 4. Main Content Frame (Row of Drinks and Controls)
        main_frame = ft.Row(
            controls=[drinks_frame, controls_frame],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        self.themed_widgets["main_frame"] = main_frame

        # 5. Status Bar
        self.themed_widgets["status_bar"] = ft.Container(
            content=self.status_text,
            padding=ft.padding.only(left=10),
            margin=ft.margin.symmetric(horizontal=10),
            height=30,
            alignment=ft.alignment.center_left,
            border_radius=5
        )

    # --- Theme Logic ---
    def toggle_theme(self, e):
        self.current_theme = "Dark" if e.control.value else "Light"
        self._apply_theme(self.current_theme)
        self.update()

    def _apply_theme(self, mode):
        colors = CafeColors.THEMES[mode]

        # Use page.bgcolor for window BG
        if self.page:
            self.page.bgcolor = colors["window_bg"]

        # Apply colors to all tracked widgets
        self.themed_widgets["header_frame"].bgcolor = colors["header_bg"]
        self.themed_widgets["header_label"].color = colors["header_text"]

        self.themed_widgets["drinks_frame"].bgcolor = colors["frame_bg"]
        self.themed_widgets["controls_frame"].bgcolor = colors["frame_bg"]
        self.themed_widgets["drinks_label"].color = colors["text"]
        self.themed_widgets["controls_label"].color = colors["text"]

        for btn_container in self.themed_widgets["drink_buttons"]:
            btn_container.bgcolor = colors["drink_fg"]
            btn_container.content.color = colors["drink_text"]
            btn_container.data = {"hover": colors["drink_hover"], "default": colors["drink_fg"]}
            btn_container.on_hover = self.on_hover_effect

        self.themed_widgets["report_btn"].bgcolor = colors["control_fg"]
        self.themed_widgets["report_btn"].content.color = colors["control_text"]
        self.themed_widgets["report_btn"].data = {"hover": colors["control_hover"], "default": colors["control_fg"]}
        self.themed_widgets["report_btn"].on_hover = self.on_hover_effect

        self.themed_widgets["off_btn"].bgcolor = colors["error_fg"]
        self.themed_widgets["off_btn"].content.color = colors["control_text"]
        self.themed_widgets["off_btn"].data = {"hover": "#8F3928", "default": colors["error_fg"]}
        self.themed_widgets["off_btn"].on_hover = self.on_hover_effect

        self.themed_widgets["status_bar"].bgcolor = colors["frame_bg"]
        self.status_text.color = colors["status_text"]

    def on_hover_effect(self, e):
        if e.data == "true":
            e.control.bgcolor = e.control.data["hover"]
        else:
            e.control.bgcolor = e.control.data["default"]
        e.control.update()

    # --- Logic Methods ---
    def update_status(self, message):
        self.status_text.value = message
        self.themed_widgets["status_bar"].update()

    def show_report(self, e):
        report_message = (
            f"Water: {coffee.resources['water']}ml\n"
            f"Milk: {coffee.resources['milk']}ml\n"
            f"Coffee: {coffee.resources['coffee']}g\n"
            f"--- Profit ---\n"
            f"Money: ${money.profit:.2f}"
        )
        self.page.snack_bar.content = ft.Text(report_message)
        self.page.snack_bar.open = True
        self.page.update()
        self.update_status("Report displayed via snack bar.")

    # --- Payment Logic ---
    def get_coin_counts(self, input_fields):
        counts = {}
        for coin, field in input_fields.items():
            try:
                counts[coin] = int(field.value)
            except ValueError:
                # Update the dialog's dedicated error message (first control in content)
                self.page.dialog.content.content.controls[0].value = f"Please enter a valid number for {coin}."
                self.page.dialog.content.content.controls[0].update()
                return None
        return counts

    def run_transaction_dfa(self, drink_item, coin_counts):
        # NOTE: Assumes money.process_coins_gui(coin_counts) returns the total value
        temp_money_received = money.process_coins_gui(coin_counts)

        if temp_money_received >= drink_item.cost and coffee.is_resource_sufficient(drink_item):
            return True
        return False

    def process_payment(self, drink_item, input_fields):
        coin_counts = self.get_coin_counts(input_fields)
        if coin_counts is None:
            return

        self.page.dialog.open = False
        self.page.update()

        transaction_successful = self.run_transaction_dfa(drink_item, coin_counts)

        if transaction_successful:
            money.make_payment(drink_item.cost, coin_counts)
            coffee.make_coffee(drink_item)

            change = round(money.money_received - drink_item.cost, 2)

            if change > 0:
                self.page.snack_bar.content = ft.Text(f"✅ Success! Here is your change: ${change:.2f}")
            else:
                self.page.snack_bar.content = ft.Text("✅ Success! Enjoy your coffee.")

            self.page.snack_bar.open = True
            self.page.update()
            self.update_status(f"Success! {drink_item.name.title()} made. Profit: ${money.profit:.2f}")
        else:
            self.page.snack_bar.content = ft.Text("❌ Transaction Failed. Insufficient funds or resources.",
                                                  color=ft.colors.RED_400)
            self.page.snack_bar.open = True
            self.page.update()
            self.update_status("Transaction failed. Check machine resources.")

    def show_payment_window(self, drink_name):
        drink_item = menu_coffee.find_drink(drink_name)
        if not drink_item:
            self.update_status(f"Error: {drink_name} not available.")
            return

        mode = self.current_theme
        colors = CafeColors.THEMES[mode]

        input_fields = {}
        coin_rows = []
        for coin_name, coin_value in money.COIN_VALUES.items():
            text_field = ft.TextField(
                label=f"{coin_name.title()} (${coin_value:.2f})",
                input_filter=ft.InputFilter(r"[0-9]"),
                value="0",
                width=100,
                bgcolor=colors["drink_fg"],
                color=colors["drink_text"],
                border_color=ft.colors.TRANSPARENT  # Looks cleaner in modern UIs
            )
            input_fields[coin_name] = text_field
            coin_rows.append(
                ft.Row([ft.Text(f"{coin_name.title()}:", color=colors["text"]), text_field],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        # Dialog content setup
        dialog_content = ft.Container(
            content=ft.Column(
                controls=[
                    # 0. Dedicated status text for input validation errors
                    ft.Text("", color=ft.colors.RED_400),
                    # 1. Cost
                    ft.Text(f"Cost: ${drink_item.cost:.2f}", size=18, weight=ft.FontWeight.BOLD, color=colors["text"]),
                    ft.Divider(color=colors["control_fg"]),
                    # 2. Coin rows
                    *coin_rows
                ],
                spacing=10
            ),
            padding=20,
            bgcolor=colors["frame_bg"]
        )

        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        pay_button = ft.ElevatedButton(
            "Pay 💸",
            on_click=lambda e: self.process_payment(drink_item, input_fields),
            bgcolor=colors["control_fg"],
            color=colors["control_text"]
        )

        cancel_button = ft.TextButton("Cancel", on_click=close_dialog)

        # Create the main dialog
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Payment for {drink_item.name.title()}", color=colors["header_text"]),
            content=dialog_content,
            actions=[pay_button, cancel_button],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=colors["header_bg"]
        )
        self.page.dialog.open = True
        self.page.update()


# --- Flet Entry Point ---
def main(page: ft.Page):
    """The main entry function for the Flet application."""

    # --- Page Configuration ---
    page.title = "Classic Cafe Flet App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 600
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.DARK  # Use Dark Mode as default start

    # --- Essential Component Setup (Order is critical) ---

    # 1. Initialize Snack Bar (Must be set on the page object before use)
    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        duration=3000
    )

    # 2. Add the custom application control
    page.add(CoffeeMachineApp())


if __name__ == "__main__":
    # Use ft.run() with the function name as the first positional argument
    ft.run(main)