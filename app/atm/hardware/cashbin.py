class CashBinState:
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class CashBinInterface:
    """For implementing REAL cash bin"""
    available_money: int
    _counting_money: int
    state: str

    def __init__(self):
        pass

    def open(self):
        """Open the money counter"""
        pass

    def close(self):
        """Close the money counter"""
        pass

    def count_money(self) -> int:
        """Count the amount of money in money counter"""
        pass

    def get_available_money(self):
        """Get available money to withdraw in the cash bin"""
        pass

    def pop_money(self, amount: int) -> bool:
        """Take out some money from the cash bin"""
        pass

    def push_money(self) -> bool:
        """Put the money into the cash bin"""
        pass

    def set_counting_money(self, amount):
        """Simulate money insertion event for testing ONLY"""
        pass


class TestCashBin(CashBinInterface):
    def __init__(self, available_money: int = 1000):
        self.available_money = available_money
        self._counting_money = 0
        self.state = CashBinState.CLOSED

    def open(self):
        self._counting_money = 0
        self.state = CashBinState.OPENED

    def close(self):
        self.state = CashBinState.CLOSED

    def count_money(self) -> int:
        return self._counting_money

    def get_available_money(self):
        return self.available_money

    def pop_money(self, amount: int) -> bool:
        if self.available_money >= amount:
            self.available_money -= amount
            self._counting_money = amount
            return True
        return False

    def push_money(self) -> bool:
        self.available_money += self._counting_money
        self._counting_money = 0
        return True

    def set_counting_money(self, amount: int):
        self._counting_money = amount


