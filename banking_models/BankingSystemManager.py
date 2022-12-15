from .Account import Account
from .AccountManager import AccountManager
from .BankingSystemX import BankingSystemX


class BankingSystemManager:
    __main_menu = """1. Create an account
2. Log into account
0. Exit
"""
    __account_menu = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""

    def __init__(self) -> None:
        self.system = BankingSystemX()

    def __stop(self) -> None:
        del self.system
        print('Bye!')
        exit(0)

    def __choice_create_account(self) -> None:
        account = self.system.generate_account()
        print('Your card has been created')
        print('Your card number:')
        print(account.get_number())
        print('Your card PIN:')
        print(account.get_pin())

    def __manage_account(self, account: Account) -> None:
        manager = AccountManager(account, self.system)
        while True:
            choice = int(input(self.__account_menu))
            if choice in (1, 2, 3, 4):
                manager.manage(choice)
                if choice == 4:
                    return
            elif choice == 5:
                return print('You have successfully logged out!')
            elif choice == 0:
                self.__stop()
            else:
                print('No such action!')

    def __choice_account_login(self) -> None:
        account_number = input('Enter your card number:\n')
        pin_code = input('Enter your PIN:\n')
        print()
        account = self.system.get_account(account_number, pin_code)
        if account is None:
            print('Wrong card number or PIN!\n')
        else:
            print('You have successfully logged in!\n')
            self.__manage_account(account)

    def run(self) -> None:
        while True:
            choice = int(input(self.__main_menu))
            print()
            if choice == 1:
                self.__choice_create_account()
            elif choice == 2:
                self.__choice_account_login()
            elif choice == 0:
                self.__stop()
            else:
                print('No such action!')
            print()
