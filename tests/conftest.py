import pytest

from app.atm.controller import ATMController
from app.atm.hardware.cardreader import TestCardReader
from app.atm.hardware.cashbin import TestCashBin
from app.atm.hardware.printer import TestPrinter
from app.bank.adopter import TestBankAdopter
from app.bank.bank import Bank

# To remove PyTest Warnings (about TestClass.__init__())
TestCardReader.__test__ = False
TestCashBin.__test__ = False
TestPrinter.__test__ = False


@pytest.fixture()
def adopter():
    adopter = TestBankAdopter()
    return adopter


@pytest.fixture()
def bank():
    adopter = TestBankAdopter()
    bank = Bank(adopter=adopter)
    return bank


@pytest.fixture()
def reader():
    reader = TestCardReader()
    return reader


@pytest.fixture()
def cashbin():
    cashbin = TestCashBin()
    return cashbin


@pytest.fixture()
def printer():
    printer = TestPrinter()
    return printer


@pytest.fixture()
def controller():
    adopter = TestBankAdopter()
    bank = Bank(adopter=adopter)

    reader = TestCardReader("12345678")
    cashbin = TestCashBin()
    printer = TestPrinter()
    ctrl = ATMController(bank=bank, reader=reader, cashbin=cashbin, printer=printer)
    return ctrl
