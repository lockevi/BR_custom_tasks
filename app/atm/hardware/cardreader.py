class CardReaderStatus:
    NO_CARD = "NO_CARD"
    CARD_IN = "CARD_IN"


class CardReaderInterface:
    """For implementing REAL card reader"""
    card_number: str
    status: str

    def __init__(self):
        pass

    def read(self):
        """Read the number of the card in the card reader"""
        pass

    def eject(self):
        """Eject the card from the card reader"""
        pass

    def insert_card(self, card_number):
        """Simulate card insertion event for testing ONLY"""
        pass


class TestCardReader(CardReaderInterface):
    def __init__(self, card_number: str = ""):
        self.card_number = card_number
        self.status = CardReaderStatus.NO_CARD

    def read(self) -> str:
        return self.card_number

    def eject(self):
        self.card_number = ""
        self.status = CardReaderStatus.NO_CARD

    def insert_card(self, card_number):
        self.card_number = card_number
        self.status = CardReaderStatus.CARD_IN

