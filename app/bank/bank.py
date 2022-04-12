from typing import List, Optional
from app.bank.adopter import BankAdopterInterface
from app.errors.exceptions import InvalidIndexException


class Bank:
    """
    Manages all about financial info and Bank API
    """
    adopter: BankAdopterInterface
    card_number: str
    entered_pin: str
    token: str
    accounts: List
    selected: int

    def __init__(self, adopter: BankAdopterInterface):
        self.adopter = adopter
        self.reset()

    def is_registered(self, card_number: str) -> bool:
        """
        Check whether the card is registered or not

        :return: True if it is registered
        """
        self.card_number = card_number
        return self.adopter.is_registered(card_number)

    def validate(self, entered_pin: str, card_number: str = "") -> bool:
        """
        Check whether PIN number is correct or not

        :return: True if it is correct
        """
        if len(card_number):
            self.card_number = card_number
        self.entered_pin = entered_pin
        res, self.token = self.adopter.validate(self.card_number, entered_pin)
        return res

    def account_list(self) -> [bool, list]:
        """
        Get the information of accounts from the Bank using the token

        :return: [result: bool, accounts: list]
        """
        res, self.accounts = self.adopter.account_list(self.token)
        return [res, self.accounts]

    def select_account(self, acc_idx: int):
        """Select an account using account index in accounts list"""
        if len(self.accounts) > acc_idx >= 0:
            self.selected = acc_idx
        else:
            raise InvalidIndexException("bank.select_account()")

    def get_account(self, acc_idx: int = -1) -> dict:
        """Get account info. using account index in accounts list"""
        if acc_idx < 0 and len(self.accounts) > self.selected >= 0:
            return self.accounts[self.selected]
        elif len(self.accounts) > acc_idx >= 0:
            return self.accounts[acc_idx]
        else:
            raise InvalidIndexException("bank.get_account()")

    def update_account(self, amount: int, acc_idx: int = -1):
        """
        Change balance of the account

        :param acc_idx: account index in accounts list
        :param amount: changing amount of money
        :return: [result: bool, account: dict]
        """
        if acc_idx < 0:
            acc_idx = self.selected
        if len(self.accounts) > acc_idx >= 0:
            res, data = self.adopter.tx_update_account(self.token, acc_idx, amount)
            if res:
                # self.accounts[self.selected] = data
                self.accounts[acc_idx] = data
            return [res, data]
        else:
            raise InvalidIndexException("bank.update_account()")

    def reset(self):
        """Remove all volatile information in memory"""
        self.card_number = ""
        self.entered_pin = ""
        self.token = ""
        self.accounts = []
        self.selected = -1
