from random import randint
from typing import Optional, Any

from .Account import Account
from .BankingDBHandler import BankingDBHandler


class BankingSystemXFlags:
    STATUS_OK = 0
    ERR_SAME_ACCOUNT = 1
    ERR_NOT_LUHN_NUMBER = 2
    ERR_NO_SUCH_ACCOUNT = 3


class BankingSystemX(BankingSystemXFlags):
    BIN_NUMBER: str = "400000"
    PIN_CODE_LENGTH: int = 4
    ACCOUNT_NUMBER_LENGTH: int = 10
    handler = BankingDBHandler()

    def __init__(self) -> None:
        pass

    def _make_new_account_number(self) -> str:
        accounts_num_full = self.handler.get_all_account_numbers()
        accounts_num = [number[len(self.BIN_NUMBER):-1] for number in accounts_num_full]
        number = "".join(str(randint(0, 9)) for _ in range(self.ACCOUNT_NUMBER_LENGTH - 1))
        while number in accounts_num:
            number = "".join(str(randint(0, 9)) for _ in range(self.ACCOUNT_NUMBER_LENGTH - 1))
        return number

    def _get_luhn_value(self, sequence):
        result = 0
        for i in range(len(sequence)):
            d = int(sequence[i])
            d = d * 2 if (i + 1) % 2 != 0 else d
            d = d - 9 if d > 9 else d
            result += d
        return result

    def _make_account_number_with_chs(self, number: str) -> str:
        sequence = [c for c in (self.BIN_NUMBER + number + "0")]
        result = self._get_luhn_value(sequence)
        for i in range(0, 10):
            if (result + i) % 10 == 0:
                sequence[-1] = str(i)
        return "".join(sequence)

    def generate_account(self) -> Account:
        account_number = self._make_new_account_number()
        account_number_full = self._make_account_number_with_chs(account_number)
        pin_code = "".join(str(randint(0, 9)) for _ in range(self.PIN_CODE_LENGTH))
        new_account = Account(account_number_full, pin_code)
        self.handler.save_account(new_account)
        return new_account

    def get_account(self, account_number: str, pin_code: str) -> Optional[Account]:
        account = self.handler.get_account_by_number(account_number)
        if account is not None:
            if account.get_pin() == pin_code:
                return account
            else:
                return None
        else:
            return None

    def get_account_to_transfer(self, number: str) -> Any:
        if self._get_luhn_value(number) % 10 != 0:
            return self.ERR_NOT_LUHN_NUMBER
        account = self.handler.get_account_by_number(number)
        if account is None:
            return self.ERR_NO_SUCH_ACCOUNT
        return account

    def transfer(self, a_from: Account, a_to: Account, amount: int):
        a_from.set_balance(a_from.get_balance() - amount)
        a_to.set_balance(a_to.get_balance() + amount)
        self.handler.transfer(a_from, a_to)
        return self.STATUS_OK

    def close_account(self, account: Account) -> None:
        self.handler.delete_account(account.get_number())

    def stop(self):
        self.handler.connection.close()
