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


def test_adopter_validate_ok(adopter):
    adopter.set_bank_data(test_data)
    res, token = adopter.validate("12345678", "1234", )
    assert res == True
    assert token == "87654321"


def test_adopter_validate_fail(adopter):
    adopter.set_bank_data(test_data)
    res, token = adopter.validate("12345678", "0000", )
    assert res == False


def test_adopter_update_account_ok(adopter):
    adopter.set_bank_data(test_data)
    res, token = adopter.validate("12345678", "1234", )
    res, data = adopter.account_list(token)
    assert len(data) == 2
    assert data[0]["acc_num"] == "11112222"
    assert data[0]["balance"] == 100
    res, account = adopter.tx_update_account(token, 0, 10)
    assert res == True
    assert account["balance"] == 110
