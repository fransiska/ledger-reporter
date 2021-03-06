#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from ledgerreporter.ledger import LedgerOptions, balance, register

FILEPATH = "tests/test.ledger"
FILEPATH2 = "tests/test2.ledger"

class LedgerTest(unittest.TestCase):
    def test_balance(self):
        res = balance(LedgerOptions(files=[FILEPATH], accounts=["Expenses"]))
        self.assertListEqual(res, [
            {'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300'},
            {'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100'}
        ])

    def test_register(self):
        res = register(LedgerOptions(files=[FILEPATH], accounts=["Expenses"]))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'}
        ])

    def test_register_with_amount_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH], accounts=["Expenses"], amount="== JPY 100"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'}
        ])

    def test_register_with_multiple_files_multiple_accounts_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH,FILEPATH2], accounts=["Food","House"]))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'},
            {'date': '2021/08/14', 'payee': 'Daiso', 'account': 'Expenses:Control:House', 'commodity': 'JPY', 'quantity': '100', 'note': ' Sponge'}
        ])

    def test_register_reverse(self):
        res = register(LedgerOptions(files=[FILEPATH], accounts=["Food","House"], reverse=True))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Liabilities:Card:202109', 'commodity': 'JPY', 'quantity': '-100', 'note': ''},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Liabilities:Card:202109', 'commodity': 'JPY', 'quantity': '-300', 'note': ''}
        ])

    def test_balance_reverse(self):
        res = balance(LedgerOptions(files=[FILEPATH], accounts=["Food","House"], reverse=True))
        self.assertListEqual(res, [
            {'account': 'Liabilities:Card:202109', 'commodity': 'JPY', 'quantity': '-400'}
        ])

    def test_register_payee_and_accounts_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], accounts=["Food","House"], payee="Grocery"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'},
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'}
        ])

    def test_register_amount_and_single_account_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], accounts=["Food"], amount="== JPY 300"))
        self.assertListEqual(res, [
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'}
        ])

    def test_register_amount_and_multiple_accounts_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], accounts=["Food","House"], amount="== JPY 300"))
        self.assertListEqual(res, [
            {'date': '2021/08/13', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Fruits', 'commodity': 'JPY', 'quantity': '300', 'note': ' もも'}
        ])

    def test_register_payee_and_multiple_accounts_filtered(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], payee="Daiso", amount="== JPY 100"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Daiso', 'account': 'Expenses:Control:House', 'commodity': 'JPY', 'quantity': '100', 'note': ' Sponge'}
        ])

    def test_register_not_payee_and_amount(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], payee="not Daiso", amount="== JPY 100"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'}
        ])

    def test_register_payee_amount_accounts(self):
        res = register(LedgerOptions(files=[FILEPATH, FILEPATH2], payee="not Daiso", amount="== JPY 100", accounts="^Expenses:Control"))
        self.assertListEqual(res, [
            {'date': '2021/08/14', 'payee': 'Grocery', 'account': 'Expenses:Control:Food:Grocery:Vegetables', 'commodity': 'JPY', 'quantity': '100', 'note': ' 人参'}
        ])
