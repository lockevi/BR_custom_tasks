import pytest

from app.atm.controller import ATMStatus
from app.errors.exceptions import *

test_data = {
    "12345678": {
        "pin": "1234",
        "accounts": [
            {"acc_num": "11112222", "balance": 100, "available": True},
            {"acc_num": "33334444", "balance": 0,   "available": True},
        ]
    },
    "13572468": {
        "pin": "8888",
        "accounts": [
            {"acc_num": "11113333", "balance": 10, "available": True},
            {"acc_num": "22224444", "balance": 50, "available": True},
        ]
    },
    "00000000": {
        "pin": "0000",
        "accounts": []
    },
}


def test_controller_read_card_ok_registered_card_number(controller):
    """If card is registered, ATM is ready to get PIN number"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD


def test_controller_read_card_fail_invalid_card_number(controller):
    """CARD_NUMBER_DIGITS defines the format of a card number"""
    test_card_number = "1234"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    with pytest.raises(InvalidCardNumberException):
        controller.read_card_number()


def test_controller_read_card_fail_invalid_card_number2(controller):
    """CARD_NUMBER_DIGITS defines the format of a card number"""
    test_card_number = "123-4567"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    with pytest.raises(InvalidCardNumberException):
        controller.read_card_number()


def test_controller_read_card_fail_unregistered_card_number(controller):
    """If card is unregistered, ATM will eject the card and reset itself."""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "00000001"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    with pytest.raises(UnregisteredCardNumberException):
        controller.read_card_number()
    assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_validate_pin_number_ok(controller):
    """If PIN is correct, ATM is ready to get accounts list"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD

    is_valid = controller.validate_pin_number(test_pin_number)
    assert is_valid == True
    assert controller.status == ATMStatus.ATM_VALID_PIN


def test_controller_validate_pin_number_fail_incorrect_entered_pin(controller):
    """If PIN is not correct, ATM need to eject the card and reset itself"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "0000"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD

    with pytest.raises(IncorrectPinNumberException):
        controller.validate_pin_number(test_pin_number)
    assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_validate_pin_number_fail_invalid_entered_pin(controller):
    """If the format of entered-PIN is invalid, ERROR"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "123456"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD

    with pytest.raises(InvalidPinNumberException):
        controller.validate_pin_number(test_pin_number)


def test_controller_get_accounts_ok(controller):
    """To select an account, ATM needs to get account list from the bank"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD
    is_valid = controller.validate_pin_number(test_pin_number)
    assert is_valid == True
    assert controller.status == ATMStatus.ATM_VALID_PIN

    accounts = controller.get_accounts()
    assert accounts == test_data[test_card_number]["accounts"]


def test_controller_get_accounts_fail_no_account(controller):
    """If there is no account in the bank, ATM needs to reset itself"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "00000000"
    test_pin_number = "0000"

    controller.insert_card(test_card_number)
    assert controller.status == ATMStatus.ATM_CARD_IN
    controller.read_card_number()
    assert controller.status == ATMStatus.ATM_REGISTERED_CARD
    is_valid = controller.validate_pin_number(test_pin_number)
    assert is_valid == True
    assert controller.status == ATMStatus.ATM_VALID_PIN

    with pytest.raises(NoAccountException):
        controller.get_accounts()
    assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_get_balance_ok(controller):
    """Check the balance by ATM (compare ATM with Bank)"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            controller.select_account(0)
            balance = controller.get_balance()
            assert balance == test_data[test_card_number]["accounts"][0]["balance"]
            assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_deposit_ok(controller):
    """Check the balance before/after deposit"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 15

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_deposit = account["balance"]
            account = controller.deposit(amount)
            after_deposit = account["balance"]
            assert before_deposit != after_deposit
            assert (before_deposit + amount) == after_deposit
            assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_deposit_fail_invalid_value(controller):
    """Check the value of amount > 0 to deposit"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 0      # !!! amount > 0 !!!

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_deposit = account["balance"]
            with pytest.raises(InvalidAmountValueException):
                account = controller.deposit(amount)


def test_controller_withdraw_ok(controller):
    """Check the balance before/after withdraw"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 15

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_withdraw = account["balance"]
            account = controller.withdraw(amount)
            after_withdraw = account["balance"]

            assert before_withdraw != after_withdraw
            assert before_withdraw == (after_withdraw + amount)
            assert controller.status == ATMStatus.ATM_NO_CARD


def test_controller_withdraw_fail_invalid_value(controller):
    """Check the value of amount > 0 to withdraw"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 0      # !!! amount > 0 !!!

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_withdraw = account["balance"]
            with pytest.raises(InvalidAmountValueException):
                account = controller.withdraw(amount)


def test_controller_withdraw_fail_not_enough_money_in_account(controller):
    """Check (the value of amount) > (balance of account) to withdraw"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 500

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_withdraw = account["balance"]
            with pytest.raises(NotEnoughMoneyInAccountException):
                account = controller.withdraw(amount)


def test_controller_withdraw_fail_not_enough_money_in_cashbin(controller):
    """Check (the value of amount) > (available in cash bin) to withdraw"""
    controller.bank.adopter.set_bank_data(test_data)
    test_card_number = "12345678"
    test_pin_number = "1234"
    amount = 100
    controller.cash_bin.available_money = 50

    controller.insert_card(test_card_number)
    controller.read_card_number()
    is_valid = controller.validate_pin_number(test_pin_number)
    if is_valid:
        accounts = controller.get_accounts()
        if len(accounts) > 0:
            account = controller.select_account(0)
            before_withdraw = account["balance"]
            with pytest.raises(NotEnoughMoneyInCashBinException):
                account = controller.withdraw(amount)