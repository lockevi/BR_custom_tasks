from app.errors.exceptions import NotEnoughPaperInPrinterException


class PrinterInterface:
    """For implementing REAL receipt printer"""
    paper: int

    def __init__(self):
        pass

    def get_available_paper(self):
        """Returns the amount of available paper in the printer"""
        pass

    def print_receipt(self, data: str):
        """Print some text for the receipt"""
        pass


class TestPrinter(PrinterInterface):
    def __init__(self, paper: int = 1000):
        self.paper = paper

    def get_available_paper(self):
        """Returns current length of paper in the printer"""
        return self.paper

    def print_receipt(self, data: str):
        """
        Print some text for the receipt
        Paper in printer will be consumed by the length of text data, not by Line Feed

        :param data: string of receipt text
        """
        length = len(data)
        if length <= self.paper:
            self.paper -= length
        else:
            raise NotEnoughPaperInPrinterException(self.paper)

