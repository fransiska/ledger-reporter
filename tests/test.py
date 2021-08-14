#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from ledgerreporter.ledger import Ledger

FILEPATH = "tests/test.ledger"

class LedgerTest(unittest.TestCase):
    def test_default_balance_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="bal"
        ).call()
        self.assertEqual(res, "Expenses:Control:Food:Grocery JPY 400\nExpenses:Control:Food:Grocery:Fruits JPY 300\nExpenses:Control:Food:Grocery:Vegetables JPY 100\nLiabilities:Card:202109 JPY -400\n 0\n")

    def test_account_filtered_balance_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="bal",
            accounts="Expenses:Control"
        ).call()
        self.assertEqual(res, "Expenses:Control:Food:Grocery JPY 400\nExpenses:Control:Food:Grocery:Fruits JPY 300\nExpenses:Control:Food:Grocery:Vegetables JPY 100\n JPY 400\n")

    def test_default_csv_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="csv"
        ).call()
        self.assertEqual(res, '"2021/08/14","","Grocery","Expenses:Control:Food:Grocery:Vegetables","JPY","100",""," 人参"\n"2021/08/14","","Grocery","Liabilities:Card:202109","JPY","-100","",""\n"2021/08/13","","Grocery","Expenses:Control:Food:Grocery:Fruits","JPY","300",""," もも"\n"2021/08/13","","Grocery","Liabilities:Card:202109","JPY","-300","",""\n')

    def test_amount_and_account_filtered_csv_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="csv",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertEqual(res, '"2021/08/14","","Grocery","Expenses:Control:Food:Grocery:Vegetables","JPY","100",""," 人参"\n')

    def test_amount_filtered_plain_reg_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="reg",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertEqual(res, '2021/08/14 Grocery JPY 100  人参\n')
