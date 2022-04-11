import pytest

from app.atm.controller import ATMStatus
from app.errors.exceptions import InvalidCardNumberException, UnregisteredCardNumberException

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

