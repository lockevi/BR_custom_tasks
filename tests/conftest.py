import pytest
from app.bank.adopter import TestBankAdopter
from app.bank.bank import Bank
from app.atm.controller import ATMController
from app.atm.hardware.cardreader import TestCardReader
from app.atm.hardware.cashbin import TestCashBin
from app.atm.hardware.printer import TestPrinter


@pytest.fixture()
def adopter():
    adopter = TestBankAdopter()
    return adopter


@pytest.fixture()
def controller():
    adopter = TestBankAdopter()
    bank = Bank(adopter=adopter)

    reader = TestCardReader("12345678")
    cashbin = TestCashBin()
    printer = TestPrinter()
    ctrl = ATMController(bank=bank, reader=reader, cashbin=cashbin, printer=printer)
    return ctrl

