class Account:
    def __init__(self, number: str, pin: str, balance: int = 0) -> None:
        self._number = number
        self._pin = pin
        self._balance = balance

    def get_pin(self) -> str:
        return self._pin

    def get_number(self) -> str:
        return self._number

    def get_balance(self) -> int:
        return self._balance

    def set_balance(self, n: int):
        self._balance = n
