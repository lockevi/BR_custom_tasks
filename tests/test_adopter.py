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


def test_adopter_is_registered_ok(adopter):
    """Check whether the card is registered or not"""
    adopter.set_bank_data(test_data)
    card_number = "12345678"
    result = adopter.is_registered(card_number=card_number)
    assert result == True


def test_adopter_is_registered_fail_unregistered_card(adopter):
    """Check whether the card is registered or not"""
    adopter.set_bank_data(test_data)
    card_number = "11112222"
    result = adopter.is_registered(card_number=card_number)
    assert result == False


def test_adopter_validate_ok(adopter):
    """Check entered-PIN == PIN of user's"""
    adopter.set_bank_data(test_data)
    res, token = adopter.validate(card_number="12345678", entered_pin="1234")
    assert res == True
    assert token == "87654321"


def test_adopter_validate_fail(adopter):
    """Fails if entered-PIN != PIN of user's"""
    adopter.set_bank_data(test_data)
    res, token = adopter.validate(card_number="12345678", entered_pin="0000")
    assert res == False


def test_adopter_update_account_ok(adopter):
    """Check the change of balance in the account after update_account"""
    adopter.set_bank_data(test_data)
    res, token = adopter.validate("12345678", "1234", )
    res, data = adopter.account_list(token)
    assert len(data) == 2
    assert data[0]["acc_num"] == "11112222"
    assert data[0]["balance"] == 100
    res, account = adopter.tx_update_account(token, 0, 10)
    assert res == True
    assert account["balance"] == 110
