from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


menu_coffee = Menu()
coffee = CoffeeMaker()
money = MoneyMachine()

is_on = True

while is_on:
    choice = input(f"What would you like? {menu_coffee.get_items()} or 'off' to exit, and 'report' for a report: ")
    
    if choice == "off":
        is_on = False
        
    elif choice == "report":
        coffee.report()
        
    elif choice == "ingredients":
        a = menu_coffee.find_drink("espresso")
        b = menu_coffee.find_drink("latte")
        c = menu_coffee.find_drink("cappuccino")
        
        print(a.ingredients)
        print(b.ingredients)
        print(c.ingredients)
    
    else:
        drink = menu_coffee.find_drink(choice)
        
        if coffee.is_resource_sufficient(drink) and drink and money.make_payment(drink.cost):
            coffee.make_coffee(drink)