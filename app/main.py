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
    ctrl.insert_card(card_number=card_number)


def read_card_number():
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
    try:
        ctrl.select_account(acc_idx=acc_idx)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Select:", acc_idx)


def get_balance():
    try:
        balance = ctrl.get_balance()
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Balance:", balance)


def deposit(money: int):
    # Open money counter
    ctrl.cash_bin.open()
    # [Fake Event] money event for testing controller
    ctrl.cash_bin.set_counting_money(money)
    # Close money counter
    ctrl.cash_bin.close()
    # Count the money in money counter
    amount = ctrl.cash_bin.count_money()

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
    # Try to withdraw
    try:
        account = ctrl.withdraw(amount=amount)
    except UpdateAccountFailedException as e:
        print("[ERROR]", e)
    except Exception as e:
        print("[ERROR]", e)
    else:
        print("Account:", account)
        ctrl.cash_bin.close()


def normal_flow_balance():
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
    # app()

