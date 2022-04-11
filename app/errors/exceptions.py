class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InvalidATMStatusException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}ATM status is invalid: {self._param}{C.ENDC}"


class InvalidCardNumberException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}Card number is invalid: {self._param}{C.ENDC}"


class UnregisteredCardNumberException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}Card number is not registered: {self._param}{C.ENDC}"


class InvalidPinNumberException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}PIN number is invalid: {self._param}{C.ENDC}"


class IncorrectPinNumberException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}PIN number is incorrect: {self._param}{C.ENDC}"


class InvalidIndexException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}Used invalid index in {self._param}{C.ENDC}"


class NoAccountException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}No account exists. card={self._param}{C.ENDC}"


class InvalidAccountInfoException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}Invalid account info: {self._param}{C.ENDC}"


class InvalidAmountValueException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}Invalid amount value: {self._param}{C.ENDC}"


class InvalidAmountValueException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}Invalid amount value: {self._param}{C.ENDC}"


class UpdateAccountFailedException(Exception):
    def __str__(self):
        return f"{C.FAIL}Bank API(updated_account) failed{C.ENDC}"


class NotEnoughMoneyInCashBinException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}Cash Bin has only ${self._param}.{C.ENDC}"


class NotEnoughMoneyInAccountException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.FAIL}Your account has only ${self._param}.{C.ENDC}"


class NotEnoughPaperInPrinterException(Exception):
    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"{C.WARNING}Paper in printer: {self._param}.{C.ENDC}"