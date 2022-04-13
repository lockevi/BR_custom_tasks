from app.common.config import conf
from app.atm.controller import ATMController
from app.bank.bank import Bank
from app.bank.adopter import TestBankAdopter
from app.atm.hardware.cardreader import TestCardReader
from app.atm.hardware.cashbin import TestCashBin
from app.atm.hardware.printer import TestPrinter
from app.errors.exceptions import *

c = conf()
adopter = TestBankAdopter()
bank = Bank(adopter=adopter)

reader = TestCardReader("12345678")
cashbin = TestCashBin()
printer = TestPrinter()
ctrl = ATMController(bank=bank, reader=reader, cashbin=cashbin, printer=printer)


def set_test_data():
    """Set the test data in DB of the bank"""
    data = {
        "12345678": {
            "pin": "1234",
            "accounts": [
                {"acc_num": "11112222", "balance": 100, "available": True},
                {"acc_num": "33334444", "balance":   0, "available": True},
            ]
        },
        "13572468": {
            "pin": "8888",
            "accounts": [
                {"acc_num": "11113333", "balance": 10, "available": True},
                {"acc_num": "22224444", "balance": 50, "available": True},
            ]
        },
    }
    adopter.set_bank_data(data)


def insert_card(card_number:str):
    """Substitute the card insertion event"""
    ctrl.insert_card(card_number=card_number)


def read_card_number():
    """
    After a card is inserted, card reader starts to read the number of that card.

    If that card was not registered in the bank, it's not possible to work.
    """
    try:
        card_number = ctrl.read_card_number()
    except UnregisteredCardNumberException as e:
        print("[WARNING]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Card Number:", card_number)
        return card_number


def validate_pin_number(entered_pin: str):
    """Check entered-PIN == PIN in the bank"""
    try:
        is_valid = ctrl.validate_pin_number(entered_pin="8888")
    except IncorrectPinNumberException as e:
        print("[WARNING]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("PIN Validation:", entered_pin, is_valid)
        return is_valid


def get_accounts():
    """Get all information of accounts related to the card from the bank"""
    try:
        accounts = ctrl.get_accounts()
    except NoAccountException as e:
        print("[WARNING]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Accounts:", accounts)
        return accounts


def select_account(acc_idx: int):
    """User selected one of account in the accounts list"""
    try:
        ctrl.select_account(acc_idx=acc_idx)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Select:", acc_idx)


def get_balance():
    """
    User chose [CHECK BALANCE] in the menu

    1. ATM sent a request to the bank.
    2. If ok, ATM shows the current balance of the account.
    3. ATM prints the receipt.
    4. ATM returns to initial state.
    """
    try:
        balance = ctrl.get_balance()
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Balance:", balance)


def deposit(money: int):
    """
    User chose [DEPOSIT] in the menu

    1. The door of money counter opened.
    2. The door of money counter closed.
    3. ATM counts the amount of money in money counter.
    4. ATM sent a request to the bank.
    5. If ok, ATM prints the receipt.
    6. ATM returns to initial state.
    """
    # Open money counter
    ctrl.open_door()
    # [Fake Event] money event for testing controller
    ctrl.cash_bin.set_counting_money(money)
    # Close money counter
    ctrl.close_door()
    # Count the money in money counter
    amount = ctrl.count_money()

    # Try to deposit
    try:
        account = ctrl.deposit(amount=amount)
    except UpdateAccountFailedException as e:
        print("[ERROR]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Account:", account)


def withdraw(amount: int):
    """
    User chose [WITHDRAW] in the menu

    1. ATM sent a request to the bank.
    2. If ok, take out that amount of money from the cash bin.
    3. The door of money counter opened.
    4. ATM prints receipt.
    5. ATM ejects the card.
    6. The door of money counter closed.
    7. ATM returns to initial state.
    """
    # Try to withdraw
    try:
        account = ctrl.withdraw(amount=amount)
    except UpdateAccountFailedException as e:
        print("[ERROR]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Account:", account)
        ctrl.close_door()


def normal_flow_balance():
    """
    User tries to check the balance of the account.

    1. Insert a card
    2. Enter PIN
    3. Select an account
    4. Select [CHECK BALANCE] in the menu
    5. Watch the balance on screen.
    6. Take a receipt
    7. Take the card
    """
    print(f"\n{C.HEADER}Normal Flow: Check Balance{C.ENDC}")
    # Insert card
    insert_card(card_number="13572468")
    # Read card number
    read_card_number()
    # Enter PIN number
    validate_pin_number(entered_pin="8888")
    # Get account list
    get_accounts()
    # Select an account in the list
    select_account(0)
    # Get the balance of the selected account
    get_balance()


def normal_flow_deposit(money: int):
    """
    User tries to deposit some money.

    1. Insert a card
    2. Enter PIN
    3. Select an account
    4. Select [DEPOSIT] in the menu
    5. Put some money to deposit
    6. Take a receipt
    7. Take the card
    """
    print(f"\n{C.HEADER}Normal Flow: Deposit({money}){C.ENDC}")
    # Insert card
    insert_card(card_number="13572468")
    # Read card number
    read_card_number()
    # Enter PIN number
    validate_pin_number(entered_pin="8888")
    # Get account list
    get_accounts()
    # Select an account in the list
    select_account(0)
    # Put money into money counter & Deposit it
    deposit(money)


def normal_flow_withdraw(amount: int):
    """
    User tries to withdraw some money.

    1. Insert a card
    2. Enter PIN
    3. Select an account
    4. Select [WITHDRAW] in the menu
    5. Input the amount of money to withdraw
    6. Take the money out of money counter
    7. Take a receipt
    8. Take the card
    """
    print(f"\n{C.HEADER}Normal Flow: Withdraw({amount}){C.ENDC}")
    # Insert card
    insert_card(card_number="13572468")
    # Read card number
    read_card_number()
    # Enter PIN number
    validate_pin_number(entered_pin="8888")
    # Get account list
    get_accounts()
    # Select an account in the list
    select_account(1)
    # Put money into money counter & Deposit it
    withdraw(amount=amount)


if __name__ == "__main__":
    set_test_data()
    normal_flow_balance()
    normal_flow_deposit(10)
    normal_flow_withdraw(25)


