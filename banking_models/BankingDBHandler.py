import sqlite3
from sqlite3 import Error
from typing import Optional

from .Account import Account


class BankingDBHandler:
    db_file = 'card.s3db'
    db_table = 'card'
    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {db_table} (
                                            id INTEGER NOT  NULL,
                                            number TEXT,
                                            pin TEXT,
                                            balance INTEGER DEFAULT 0
                                        ); """
    sql_get_last_id = f"SELECT id FROM {db_table} ORDER BY id DESC LIMIT 1;"
    sql_get_all_accounts = f"SELECT number FROM {db_table};"
    sql_insert_statement = f"INSERT INTO {db_table} (id, number, pin, balance) VALUES (?, ?, ?, ?);"
    sql_find_by_num_statement = f"SELECT * FROM {db_table} WHERE number = ?;"
    sql_update_amount = f"UPDATE {db_table} SET balance = ? WHERE number = ?;"
    sql_delete_account = f"DELETE FROM {db_table} WHERE number = ?;"
    sql_transaction_begin = "BEGIN TRANSACTION;"
    sql_transaction_commit = "COMMIT;"
    sql_transfer_from_to = f"""
                    BEGIN TRANSACTION;
                    {sql_update_amount}
                    {sql_update_amount}
                    COMMIT;"""

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.sql_create_table)
            self.connection.commit()

            last_id = self.cursor.execute(self.sql_get_last_id).fetchone()
            self.last_id = last_id[0] if last_id is not None else 0
        except Error as e:
            print(e)

    def save_account(self, account: Account) -> None:
        self.last_id += 1
        new_id = self.last_id
        number = account.get_number()
        pin = account.get_pin()
        balance = account.get_balance()
        self.cursor.execute(self.sql_insert_statement, (new_id, number, pin, balance))
        self.connection.commit()

    def get_all_account_numbers(self) -> list:
        accounts = self.cursor.execute(self.sql_get_all_accounts).fetchall()
        if len(accounts) != 0:
            return [acc[0] for acc in accounts]
        return []

    def get_account_by_number(self, num: str) -> Optional[Account]:
        data = self.cursor.execute(self.sql_find_by_num_statement, [num, ]).fetchone()
        if data is None:
            return None
        number = data[1]
        pin = data[2]
        balance = data[3]
        return Account(number, pin, balance)

    def get_all(self):
        return self.cursor.execute(f"select * from {self.db_table};").fetchall()

    def transfer(self, acc_from: Account, acc_to: Account):
        self.cursor.execute(self.sql_transaction_begin)
        self.cursor.execute(self.sql_update_amount,
                            [acc_from.get_balance(), acc_from.get_number()])
        self.cursor.execute(self.sql_update_amount,
                            [acc_to.get_balance(), acc_to.get_number()])
        self.cursor.execute(self.sql_transaction_commit)

    def update_account(self, account: Account) -> None:
        self.cursor.execute(
            self.sql_update_amount,
            [account.get_balance(), account.get_number()])
        self.connection.commit()

    def delete_account(self, number: str) -> None:
        self.cursor.execute(self.sql_transaction_begin)
        self.cursor.execute(self.sql_delete_account, [number, ])
        self.cursor.execute(self.sql_transaction_commit)
