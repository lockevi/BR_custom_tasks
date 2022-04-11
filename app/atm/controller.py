from app.common.consts import CARD_NUMBER_DIGITS, PIN_NUMBER_DIGITS
from app.bank.bank import Bank
from app.atm.hardware.cardreader import CardReaderInterface
from app.atm.hardware.cashbin import CashBinInterface
from app.atm.hardware.printer import PrinterInterface
from app.errors.exceptions import *


class ATMStatus:
    ATM_NEED_MAINTENANCE = -1  # "NEED_MAINTENANCE"
    ATM_INIT = 0  # "INITIALIZING"
    ATM_NO_CARD = 10  # "NO_CARD_INSERTED"
    ATM_CARD_IN = 20  # "CARD_INSERTED"
    ATM_REGISTERED_CARD = 21  # "REGISTERED_CARD"
    ATM_VALID_PIN = 30  # "VALID_PIN"
    ATM_ACCOUNTS_READY = 40  # "ACCOUNTS_READY"
    ATM_ACCOUNT_SELECTED = 41  # "ACCOUNT_SELECTED"


class ATMController:
    """Basic ATM Controller Class"""
    bank: Bank
    """Interface to the bank"""
    card_reader: CardReaderInterface
    """Interface to card reader hardware"""
    cash_bin: CashBinInterface
    """Interface to cash bin hardware"""
    printer: PrinterInterface
    """Interface to receipt printer hardware"""
    status: int
    """Status of ATM Controller"""

    def __init__(self,
                 bank: Bank,
                 reader: CardReaderInterface,
                 cashbin: CashBinInterface,
                 printer: PrinterInterface):
        self.bank = bank
        self.card_reader = reader
        self.cash_bin = cashbin
        self.printer = printer
        self.status = ATMStatus.ATM_NO_CARD

    def insert_card(self, card_number: str):
        """
        Virtually, insert card for test
        """
        self.card_reader.insert_card(card_number)
        self.status = ATMStatus.ATM_CARD_IN

    def read_card_number(self) -> str:
        """
        Read the number of the card in card reader hardware

        :return: the string of numbers of inserted card
        """
        # Check: ATM Status
        if self.status < ATMStatus.ATM_CARD_IN:
            raise InvalidATMStatusException(self.status)
        card_number = self.card_reader.read()
        if card_number.isdecimal() and len(card_number) == CARD_NUMBER_DIGITS:
            # Check: is it registered?
            if self.bank.is_registered(card_number):
                self.status = ATMStatus.ATM_REGISTERED_CARD
                return card_number
            else:
                self.reset()
                raise UnregisteredCardNumberException("Unregistered Card")

        else:
            raise InvalidCardNumberException(card_number)

    def validate_pin_number(self, entered_pin: str):
        """
        Ask entered-PIN's validity to the bank

        :param entered_pin: PIN entered from UI
        :return: PIN is correct(True) or not(False)
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_REGISTERED_CARD:
            raise InvalidATMStatusException(self.status)
        # Check PIN number format
        if entered_pin.isdecimal() and len(entered_pin) == PIN_NUMBER_DIGITS:
            if self.bank.validate(entered_pin=entered_pin):
                self.status = ATMStatus.ATM_VALID_PIN
                return True
            else:
                raise IncorrectPinNumberException(entered_pin)
                # return False
        else:
            raise InvalidPinNumberException(entered_pin)

    def get_accounts(self) -> list:
        """
        Get a list of accounts from the bank

        :return: List of accounts
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_VALID_PIN:
            raise InvalidATMStatusException(self.status)
        res, accounts = self.bank.account_list()
        if len(accounts) > 0:
            self.status = ATMStatus.ATM_ACCOUNTS_READY
            return accounts
        else:
            # If there is no account, ATM ejects card and reset itself.
            self.reset()
            raise NoAccountException(self.bank.card_number)

    def select_account(self, acc_idx: int):
        """
        Select an account to GetBalance, Deposit or Withdraw

        :param acc_idx: selected index of accounts list
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNTS_READY:
            raise InvalidATMStatusException(self.status)
        self.bank.select_account(acc_idx)
        self.status = ATMStatus.ATM_ACCOUNT_SELECTED

    def get_balance(self) -> int:
        """
        Get the balance of the selected account

        :return: current balance of the account
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNT_SELECTED:
            raise InvalidATMStatusException(self.status)
        account = self.bank.get_account()
        if "balance" in account:
            # At the end of workflow, print a receipt and reset itself.
            self.printer.print_receipt(str(account["balance"]))
            self.reset()
            return account["balance"]
        else:
            raise InvalidAccountInfoException(account)

    def deposit(self, amount: int) -> dict:
        """
        Update the bank account for deposit

        :param amount: the amount of money in the money counter
        :return: updated account info.
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNT_SELECTED:
            raise InvalidATMStatusException(self.status)
        # Check the value of amount
        if amount <= 0:
            raise InvalidAmountValueException(amount)
        # Update account of the bank
        res, account = self.bank.update_account(acc_idx=self.bank.selected, amount=amount)
        if res:
            self.cash_bin.push_money()
            self.printer.print_receipt(str(account))
            self.reset()
            return account
        else:
            self.cash_bin.open()
            self.reset()
            raise UpdateAccountFailedException()

    def withdraw(self, amount: int) -> dict:
        """
        Update the bank account for withdraw

        :param amount: the amount of money to withdraw
        :return: updated account info.
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNT_SELECTED:
            raise InvalidATMStatusException(self.status)
        # Check the value of amount
        if amount <= 0:
            raise InvalidAmountValueException(amount)
        # Check the balance of the selected account
        current_balance = self.bank.get_account()["balance"]
        if amount > current_balance:
            self.reset()
            raise NotEnoughMoneyInAccountException(current_balance)
        # Check available money in the cash bin
        if amount > self.cash_bin.available_money:
            self.reset()
            raise NotEnoughMoneyInCashBinException(self.cash_bin.available_money)

        # Update account of the bank (amount = -amount)
        res, account = self.bank.update_account(acc_idx=self.bank.selected, amount=-amount)
        if res:
            self.cash_bin.pop_money(amount=amount)
            self.cash_bin.open()
            self.printer.print_receipt(str(account))
            self.reset()
            return account
        else:
            self.reset()
            raise UpdateAccountFailedException()

    def reset(self):
        """
        Ejects card & Return to initial state
        """
        self.card_reader.eject()
        self.bank.reset()
        self.status = ATMStatus.ATM_NO_CARD

    def open_door(self):
        self.cash_bin.open()

    def close_door(self):
        self.cash_bin.close()

    def count_money(self) -> int:
        count = self.cash_bin.count_money()
        return count

    def send_diagnosis(self):
        pass
