import pytest

from app.errors.exceptions import InvalidIndexException

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


def test_bank_is_registered_ok(bank):
    """Check whether the card is registered or not"""
    bank.adopter.set_bank_data(test_data)
    card_number = "12345678"
    result = bank.is_registered(card_number=card_number)
    assert result == True
    assert bank.card_number == card_number


def test_bank_is_registered_fail_unregistered_card(bank):
    """Check whether the card is registered or not"""
    bank.adopter.set_bank_data(test_data)
    card_number = "11112222"
    result = bank.is_registered(card_number=card_number)
    assert result == False
    assert bank.card_number == card_number


def test_adopter_validate_ok(bank):
    """Check entered-PIN == PIN of user's"""
    bank.adopter.set_bank_data(test_data)
    result = bank.validate(card_number="12345678", entered_pin="1234")
    assert result == True
    assert bank.token == "87654321"


def test_adopter_validate_fail_incorrect_pin(bank):
    """Fails if entered-PIN != PIN of user's"""
    bank.adopter.set_bank_data(test_data)
    result = bank.validate(card_number="12345678", entered_pin="0000")
    assert result == False
    assert bank.token == ""


def test_bank_select_account_fail_invalid_index(bank):
    """Check selected account index >= len(accounts)"""
    bank.adopter.set_bank_data(test_data)
    validation = bank.validate(card_number="12345678", entered_pin="1234")
    assert validation == True
    result, accounts = bank.account_list()
    assert result == True
    assert len(accounts) == 2
    with pytest.raises(InvalidIndexException):
        bank.select_account(3)


def test_bank_update_account_ok(bank):
    """Check the change of balance in the account after update_account"""
    bank.adopter.set_bank_data(test_data)
    validation = bank.validate(card_number="12345678", entered_pin="1234")
    assert validation == True
    result, accounts = bank.account_list()
    assert result == True
    assert len(accounts) == 2
    assert accounts[0]["acc_num"] == "11112222"
    assert accounts[0]["balance"] == 100
    result, account = bank.update_account(acc_idx=0, amount=10)
    assert result == True
    assert account["balance"] == 110


def test_bank_reset_ok(bank):
    """All financial information should be removed after reset"""
    bank.adopter.set_bank_data(test_data)
    validation = bank.validate(card_number="12345678", entered_pin="1234")
    result, accounts = bank.account_list()
    bank.select_account(1)
    result, account = bank.update_account(amount=10)
    assert result == True
    assert account["balance"] == 10

    bank.reset()
    assert bank.card_number == ""
    assert bank.entered_pin == ""
    assert bank.token == ""
    assert bank.accounts == []
    assert bank.selected < 0

