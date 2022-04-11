from typing import List


class BankAdopterInterface:
    """For implementing Real Bank API"""
    def __init__(self):
        pass

    def is_registered(self, card_number: str):
        """Check availability of the card number"""
        pass

    def validate(self, card_number: str, entered_pin: str):
        """Check validity of the entered-PIN number"""
        pass

    def account_list(self, token: str):
        """Get a list of all accounts related to the card number"""
        pass

    def tx_update_account(self, token: str, acc_idx: int, amount: int):
        """Update account info. for deposit or withdraw"""
        pass


class TestBankAdopter(BankAdopterInterface):
    """For testing on local env."""
    bank_data: dict
    # data = {
    #     "12345678": {
    #         "pin": "1234",
    #         "accounts": [
    #             {"acc_num": "11112222", "balance": 100, "available": True},
    #             {"acc_num": "33334444", "balance": 0, "available": True},
    #         ]
    #     },
    # }

    def __init__(self):
        super().__init__()
        self.bank_data = {}  # key(card_num), value({pin, [accounts]})

    def is_registered(self, card_number: str) -> bool:
        return card_number in self.bank_data

    def validate(self, card_number: str, entered_pin: str) -> List:
        # print("adoter.validate() : ", card_number, entered_pin)
        if card_number in self.bank_data:
            pin = self.bank_data[card_number]["pin"]
            if pin == entered_pin:
                token = card_number[::-1]   # use reversed card_number as a token
                return [True, token]
        return [False, ""]

    def account_list(self, token: str) -> List:
        card_number = token[::-1]           # use reversed card_number as a token
        if card_number in self.bank_data:
            if "accounts" in self.bank_data[card_number]:
                return [True, self.bank_data[card_number]["accounts"]]
        return [False, []]

    def tx_update_account(self, token: str, acc_idx: int, amount: int) -> List:
        card_number = token[::-1]  # use reversed card_number as a token
        if card_number in self.bank_data:
            if "accounts" in self.bank_data[card_number]:
                accounts = self.bank_data[card_number]["accounts"]
                if len(accounts) > acc_idx >= 0:
                    acc = accounts[acc_idx]
                    acc["balance"] += amount
                    return [True, acc]
        return [False, None]

    def set_bank_data(self, data: dict):
        """For testing only (instead of DB)"""
        self.bank_data = data

