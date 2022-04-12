from app.atm.hardware.cardreader import TestCardReader, CardReaderStatus
from app.common.consts import CARD_NUMBER_DIGITS


def test_cardreader_ok_initial_status():
    """There is no card in card reader at initial status"""
    reader = TestCardReader()
    assert reader.status == CardReaderStatus.NO_CARD


def test_cardreader_read_ok(reader):
    """Check the card reader reads the number of the card properly"""
    fake_card = "0000111122223333"
    # [FAKE] simulate card insertion event
    reader.insert_card(fake_card)

    card_number = reader.read()
    assert card_number == fake_card
    assert reader.status == CardReaderStatus.CARD_IN


def test_cardreader_read_ok_no_check_format(reader):
    """Card reader does not check the format of card number"""
    fake_card = "1111"
    # [FAKE] simulate card insertion event
    reader.insert_card(fake_card)

    card_number = reader.read()
    assert card_number == fake_card
    assert reader.status == CardReaderStatus.CARD_IN
    assert len(fake_card) != CARD_NUMBER_DIGITS

