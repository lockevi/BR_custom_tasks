import pytest

from app.atm.hardware.printer import TestPrinter
from app.errors.exceptions import NotEnoughPaperInPrinterException


def test_printer_get_available_paper_ok():
    """Check the available paper in the printer"""
    printer = TestPrinter(paper=333)
    paper = printer.get_available_paper()
    assert paper == 333


def test_printer_print_receipt_ok(printer):
    """Check the change of available paper in printer after printing receipt"""
    receipt_text = "ACCOUNT: 11112222XXXXXXXX\nBALANCE: 1000\nDATE: 04/12/2022\n..."
    before_print = printer.get_available_paper()
    printer.print_receipt(receipt_text)
    after_print = printer.get_available_paper()
    assert before_print == (after_print + len(receipt_text))


def test_printer_print_receipt_fail_not_enough_paper():
    """If available < length of receipt, the request will FAIL."""
    printer = TestPrinter(paper=15)
    receipt_text = "ACCOUNT: 11112222XXXXXXXX\nBALANCE: 1000\nDATE: 04/12/2022\n..."

    before_print = printer.get_available_paper()
    with pytest.raises(NotEnoughPaperInPrinterException):
        printer.print_receipt(receipt_text)
    after_print = printer.get_available_paper()
    assert before_print == after_print

