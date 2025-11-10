class MoneyMachine:

    CURRENCY = "$"

    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01
    }

    def __init__(self):
        self.profit = 0
        self.money_received = 0

    def report(self):
        """Prints the current profit"""
        print(f"Money: {self.CURRENCY}{self.profit}")

        # ... (rest of the class remains the same)

    def process_coins_gui(self, coin_counts):
        """Calculates the total from coin counts provided by the GUI."""
        self.money_received = 0
        for coin, count in coin_counts.items():
            if coin in self.COIN_VALUES:
                self.money_received += count * self.COIN_VALUES[coin]
        return self.money_received

    def make_payment(self, cost, coin_counts=None):
        """Returns True when payment is accepted, or False if insufficient.
           It uses coin_counts (from GUI) if provided, otherwise defaults to CLI input."""

        # Use GUI input if coin_counts is provided
        if coin_counts is not None:
            self.process_coins_gui(coin_counts)
        # Fallback to original CLI process_coins() if needed (though not used in this GUI version)
        # else:
        #     self.process_coins()

        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            # Use messagebox for change display instead of print()
            print(f"Here is ${change} in change.")
            self.profit += cost
            self.money_received = 0
            return True
        else:
            # Use messagebox for insufficient funds display instead of print()
            print("Sorry that's not enough money. Money refunded.")
            self.money_received = 0
            return False
