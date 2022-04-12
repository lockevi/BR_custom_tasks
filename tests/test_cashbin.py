from app.atm.hardware.cashbin import TestCashBin, CashBinState


def test_cashbin_get_available_money_ok():
    """Check the available money in the cash bin"""
    cashbin = TestCashBin(available_money=333)
    money_in_cashbin = cashbin.get_available_money()
    assert money_in_cashbin == 333


def test_cashbin_open_close_ok(cashbin):
    """Check the door functionality (open/close)"""
    # initial state
    assert cashbin.state == CashBinState.CLOSED
    cashbin.open()      # door opened
    assert cashbin.state == CashBinState.OPENED
    cashbin.close()     # door closed
    assert cashbin.state == CashBinState.CLOSED


def test_cashbin_count_money_ok(cashbin):
    """Count money in the money counter from user"""
    cashbin.open()  # door opened
    # [FAKE] put some money into money counter
    cashbin.set_counting_money(amount=10)
    cashbin.close() # door closed

    # Count the money in money counter
    counted_money = cashbin.count_money()
    assert counted_money == 10


def test_cashbin_push_money_ok():
    """Check the change of available money in cash bin after deposit"""
    cashbin = TestCashBin(available_money=100)
    cashbin.open()  # door opened
    # [FAKE] put some money into money counter
    cashbin.set_counting_money(amount=10)
    cashbin.close()  # door closed
    # Count the money in money counter
    money_input = cashbin.count_money()
    before_push = cashbin.get_available_money()

    # push that money into cash bin
    cashbin.push_money()
    after_push = cashbin.get_available_money()
    assert after_push == (before_push + money_input)


def test_cashbin_pop_money_ok(cashbin):
    """Check the change of available money in cash bin after withdraw"""
    before_pop = cashbin.get_available_money()
    # pop some money from cash bin
    cashbin.pop_money(amount=10)
    cashbin.open()      # door opened
    cashbin.close()     # door closed
    after_pop = cashbin.get_available_money()
    assert after_pop == (before_pop - 10)


def test_cashbin_pop_money_fail_not_enough_money():
    """If available < amount to withdraw, the request will FAIL."""
    cashbin = TestCashBin(available_money=100)
    # try to pop too much money greater than available in cash bin
    result = cashbin.pop_money(amount=200)
    assert result == False





