from app.common.consts import CARD_NUMBER_DIGITS, PIN_NUMBER_DIGITS
from app.bank.bank import Bank
from app.atm.hardware.cardreader import CardReaderInterface
from app.atm.hardware.cashbin import CashBinInterface
from app.atm.hardware.printer import PrinterInterface
from app.errors.exceptions import *
from app.utils.logger import logger


class ATMStatus:
    ATM_NEED_MAINTENANCE = -1   # "NEED_MAINTENANCE"
    ATM_INIT = 0                # "INITIALIZING"
    ATM_NO_CARD = 10            # "NO_CARD_INSERTED"
    ATM_CARD_IN = 20            # "CARD_INSERTED"
    ATM_REGISTERED_CARD = 21    # "REGISTERED_CARD"
    ATM_VALID_PIN = 30          # "VALID_PIN"
    ATM_ACCOUNTS_READY = 40     # "ACCOUNTS_READY"
    ATM_ACCOUNT_SELECTED = 41   # "ACCOUNT_SELECTED"


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
        logger.info(f"INSERTED_CARD:{card_number}")

    def read_card_number(self) -> str:
        """
        Read the number of the card in card reader hardware

        :return: the string of numbers of inserted card
        """
        # Check: ATM Status
        if self.status < ATMStatus.ATM_CARD_IN:
            logger.error(f"INVALID_STATUS:{self.status} at read_card_number")
            raise InvalidATMStatusException(self.status)
        card_number = self.card_reader.read()
        if card_number.isdecimal() and len(card_number) == CARD_NUMBER_DIGITS:
            # Check: is it registered?
            if self.bank.is_registered(card_number):
                self.status = ATMStatus.ATM_REGISTERED_CARD
                logger.info(f"REGISTERED_CARD:{card_number}")
                return card_number
            else:
                logger.info(f"UNREGISTERED_CARD:{card_number}")
                self.reset()
                raise UnregisteredCardNumberException("Unregistered Card")

        else:
            logger.error(f"INVALID_CARD_FORMAT:{card_number}")
            raise InvalidCardNumberException(card_number)

    def validate_pin_number(self, entered_pin: str):
        """
        Ask entered-PIN's validity to the bank

        :param entered_pin: PIN entered from UI
        :return: PIN is correct(True) or not(False)
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_REGISTERED_CARD:
            logger.error(f"INVALID_STATUS:{self.status} at validate_pin_number")
            raise InvalidATMStatusException(self.status)
        # Check PIN number format
        if entered_pin.isdecimal() and len(entered_pin) == PIN_NUMBER_DIGITS:
            if self.bank.validate(entered_pin=entered_pin):
                self.status = ATMStatus.ATM_VALID_PIN
                logger.info(f"PIN_IS_CORRECT")
                return True
            else:
                logger.info(f"PIN_IS_INCORRECT")
                self.reset()
                raise IncorrectPinNumberException(entered_pin)
                # return False
        else:
            logger.error(f"INVALID_PIN_FORMAT:{entered_pin}")
            raise InvalidPinNumberException(entered_pin)

    def get_accounts(self) -> list:
        """
        Get a list of accounts from the bank

        :return: List of accounts
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_VALID_PIN:
            logger.error(f"INVALID_STATUS:{self.status} at get_accounts")
            raise InvalidATMStatusException(self.status)
        res, accounts = self.bank.account_list()
        if len(accounts) > 0:
            self.status = ATMStatus.ATM_ACCOUNTS_READY
            logger.info(f"ACCOUNTS_DATA: {accounts}")
            return accounts
        else:
            # If there is no account, ATM ejects card and reset itself.
            logger.info(f"NO_ACCOUNTS")
            self.reset()
            raise NoAccountException(self.bank.card_number)

    def select_account(self, acc_idx: int) -> dict:
        """
        Select an account to GetBalance, Deposit or Withdraw

        :param acc_idx: selected index of accounts list
        :return: dict: selected account info
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNTS_READY:
            logger.error(f"INVALID_STATUS:{self.status} at select_account")
            raise InvalidATMStatusException(self.status)
        account = self.bank.select_account(acc_idx)
        self.status = ATMStatus.ATM_ACCOUNT_SELECTED
        logger.info(f"ACCOUNT_SELECTED: {acc_idx}")
        return account

    def get_balance(self) -> int:
        """
        Get the balance of the selected account

        :return: int: current balance of the account
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNT_SELECTED:
            logger.error(f"INVALID_STATUS:{self.status} at get_balance")
            raise InvalidATMStatusException(self.status)
        logger.info(f"BANK_BALANCE_START")
        account = self.bank.get_account()
        if "balance" in account:
            logger.info(f"BANK_BALANCE_OK")
            # At the end of workflow, print a receipt and reset itself.
            self.printer.print_receipt(str(account["balance"]))
            logger.info(f"PRINT_RECEIPT")
            self.reset()
            return account["balance"]
        else:
            logger.error(f"INVALID_ACCOUNT_INFO")
            raise InvalidAccountInfoException(account)

    def deposit(self, amount: int) -> dict:
        """
        Update the bank account for deposit

        :param amount: the amount of money in the money counter
        :return: updated account info.
        """
        # Check ATM Status
        if self.status < ATMStatus.ATM_ACCOUNT_SELECTED:
            logger.error(f"INVALID_STATUS:{self.status} at deposit")
            raise InvalidATMStatusException(self.status)
        # Check the value of amount
        if amount <= 0:
            logger.error(f"INVALID_DEPOSIT_VALUE:{amount}")
            raise InvalidAmountValueException(amount)
        logger.info(f"BANK_DEPOSIT_START")
        # Update account of the bank
        res, account = self.bank.update_account(acc_idx=self.bank.selected, amount=amount)
        if res:
            logger.info(f"BANK_DEPOSIT_OK")
            self.cash_bin.push_money()
            logger.info(f"PUSH_MONEY")
            self.printer.print_receipt(str(account))
            logger.info(f"PRINT_RECEIPT")
            self.reset()
            return account
        else:
            logger.error(f"BANK_DEPOSIT_FAIL")
            self.cash_bin.open()
            logger.info(f"DOOR_OPENED")
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
            logger.error(f"INVALID_STATUS:{self.status} at withdraw")
            raise InvalidATMStatusException(self.status)
        # Check the value of amount
        if amount <= 0:
            logger.error(f"INVALID_WITHDRAW_VALUE:{amount}")
            raise InvalidAmountValueException(amount)
        # Check the balance of the selected account
        current_balance = self.bank.get_account()["balance"]
        if amount > current_balance:
            logger.info(f"NOT_ENOUGH_MONEY_IN_ACCOUNT:{amount} > {current_balance}")
            self.reset()
            raise NotEnoughMoneyInAccountException(current_balance)
        # Check available money in the cash bin
        if amount > self.cash_bin.available_money:
            logger.info(f"NOT_ENOUGH_MONEY_IN_CASH_BIN:{amount} > {self.cash_bin.available_money}")
            self.reset()
            raise NotEnoughMoneyInCashBinException(self.cash_bin.available_money)
        logger.info(f"BANK_WITHDRAW_START")
        # Update account of the bank (amount = -amount)
        res, account = self.bank.update_account(acc_idx=self.bank.selected, amount=-amount)
        if res:
            logger.info(f"BANK_WITHDRAW_OK")
            self.cash_bin.pop_money(amount=amount)
            logger.info(f"POP_MONEY")
            self.cash_bin.open()
            logger.info(f"DOOR_OPENED")
            self.printer.print_receipt(str(account))
            logger.info(f"PRINT_RECEIPT")
            self.reset()
            return account
        else:
            logger.info(f"BANK_WITHDRAW_FAIL")
            self.reset()
            raise UpdateAccountFailedException()

    def reset(self):
        """
        Ejects card & Return to initial state
        """
        self.card_reader.eject()
        logger.info(f"EJECTED_CARD")
        self.bank.reset()
        self.status = ATMStatus.ATM_NO_CARD
        logger.info(f"RESET\n")

    def open_door(self):
        """Open money counter"""
        self.cash_bin.open()
        logger.info(f"DOOR_OPENED")

    def close_door(self):
        """Close money counter"""
        self.cash_bin.close()
        logger.info(f"DOOR_CLOSED")

    def count_money(self) -> int:
        """Count money in money counter"""
        count = self.cash_bin.count_money()
        logger.info(f"MONEY_COUNTED: {count}")
        return count

    def send_diagnosis(self):
        """Send diagnosis data for remote monitoring"""
        logger.info(f"SENT_DIAGNOSIS_DATA")
