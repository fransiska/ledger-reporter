#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from ledgerreporter.ledger import LedgerOptions, balance, register

FILEPATH = "tests/test.ledger"
FILEPATH2 = "tests/test2.ledger"

class LedgerTest(unittest.TestCase):
    def test_default_balance_result(self):
        res = balance(LedgerOptions(files=[FILEPATH], accounts=["Expenses"]))
        self.assertListEqual(res, [
            {'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300'},
            {'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100'}
        ])

    def test_register_result(self):
        res = register(LedgerOptions(files=[FILEPATH], accounts=["Expenses"]))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'}
        ])

    def test_register_result_amount_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH], accounts=["Expenses"], amount="== JPY 100"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'}
        ])

    def test_register_result_multiple_files_multiple_accounts_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH,FILEPATH2], accounts=["Food","House"]))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'},
            {'date': '2021/08/14', 'payee': 'Daiso', 'account': 'Expenses:Control:House', 'commodity': 'JPY', 'quantity': '100', 'note': ' Sponge'}
        ])
