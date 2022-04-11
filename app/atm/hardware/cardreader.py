class CardReaderInterface:
    """For implementing REAL card reader"""
    card_number: str

    def __init__(self):
        self.card_number = ""

    def read(self) -> str:
        return self.card_number

    def eject(self):
        self.card_number = ""

    def insert_card(self, card_number):
        pass


class TestCardReader(CardReaderInterface):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def insert_card(self, card_number):
        self.card_number = card_number

