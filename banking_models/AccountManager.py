from .Account import Account
from .BankingSystemX import BankingSystemX


class AccountManager:
    def __init__(self, account: Account, system: BankingSystemX) -> None:
        self.account = account
        self.system = system
        self.actions = {
            1: self.__show_balance,
            2: self.__add_income,
            3: self.__do_transfer,
            4: self.__close_account
        }

    def __show_balance(self) -> None:
        print(f'Balance: {self.account.get_balance()}\n')

    def __add_income(self) -> None:
        income = int(input('Enter income:\n'))
        self.account.set_balance(self.account.get_balance() + income)
        self.system.handler.update_account(self.account)

    def __do_transfer(self) -> None:
        print('Transfer')
        card_number = input('Enter card number:\n')
        account_to = self.system.get_account_to_transfer(card_number)
        if card_number == self.account.get_number():
            print('You can\'t transfer money to the same account!')
        elif account_to == self.system.ERR_NOT_LUHN_NUMBER:
            print('Probably you made a mistake in the card number. Please try again!')
        elif account_to == self.system.ERR_NO_SUCH_ACCOUNT:
            print('Such a card does not exist.')
        else:
            amount = int(input('Enter how much money you want to transfer:\n'))
            if amount > self.account.get_balance():
                print('Not enough money!')
            else:
                response = self.system.transfer(self.account, account_to, amount)
                if response == self.system.STATUS_OK:
                    print('Success!')

    def __close_account(self) -> None:
        self.system.close_account(self.account)
        print('The account has been closed!\n')

    @staticmethod
    def __fallback() -> None:
        print('Error occurred!')

    def manage(self, option: int) -> None:
        self.actions.get(option, self.__fallback)()
