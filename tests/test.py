#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from ledgerreporter.ledger import Ledger
import ledgerreporter.reporter as reporter

FILEPATH = "tests/test.ledger"
FILEPATH2 = "tests/test2.ledger"

class LedgerTest(unittest.TestCase):
    def test_default_balance_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="bal"
        ).call()
        self.assertListEqual(res, [
            ["account", "commodity", "quantity"],
            ["Expenses:Control:Food:Grocery","JPY","400"],
            ["Expenses:Control:Food:Grocery:Fruits","JPY","300"],
            ["Expenses:Control:Food:Grocery:Vegetables","JPY","100"],
            ["Liabilities:Card:202109","JPY","-400"],
            ["", "","0"]])

    def test_account_filtered_balance_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="bal",
            accounts="Expenses:Control"
        ).call()
        self.assertEqual(res, [
            ["account", "commodity", "quantity"],
            ["Expenses:Control:Food:Grocery","JPY","400"],
            ["Expenses:Control:Food:Grocery:Fruits","JPY","300"],
            ["Expenses:Control:Food:Grocery:Vegetables","JPY","100"],
            ["", "JPY","400"]])

    def test_default_csv_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="csv"
        ).call()
        self.assertEqual(res, [
            ["date", "code", "payee", "account", "commodity", "quantity", "cleared", "note"],
            ["2021/08/14","","Grocery","Expenses:Control:Food:Grocery:Vegetables","JPY","100",""," 人参"],
            ["2021/08/14","","Grocery","Liabilities:Card:202109","JPY","-100","",""],
            ["2021/08/13","","Grocery","Expenses:Control:Food:Grocery:Fruits","JPY","300",""," もも"],
            ["2021/08/13","","Grocery","Liabilities:Card:202109","JPY","-300","",""]])

    def test_amount_filtered_csv_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="csv",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertListEqual(res, [
            ["date", "code", "payee", "account", "commodity", "quantity", "cleared", "note"],
            ["2021/08/14","","Grocery","Expenses:Control:Food:Grocery:Vegetables","JPY","100",""," 人参"]])

    def test_amount_and_account_filtered_csv_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="csv",
            accounts="Expenses:Control",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertListEqual(res, [
            ["date", "code", "payee", "account", "commodity", "quantity", "cleared", "note"],
            ["2021/08/14","","Grocery","Expenses:Control:Food:Grocery:Vegetables","JPY","100",""," 人参"]])

    def test_amount_filtered_plain_reg_result(self):
        res = Ledger(
            filepath=FILEPATH,
            command="reg",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertListEqual(res, [
            ["date", "payee", "commodity", "quantity", "note"],
            ["2021/08/14","Grocery","JPY","100"," 人参"]])

    def test_multiple_files(self):
        res = Ledger(
            filepath=[FILEPATH, FILEPATH2],
            command="reg",
            filter_by="amount",
            filter_args="JPY 100"
        ).call()
        self.assertListEqual(res, [
            ["date", "payee", "commodity", "quantity", "note"],
            ["2021/08/14","Grocery","JPY","100"," 人参"],
            ["2021/08/14","Daiso","JPY","100"," Sponge"]
        ])

    def test_multiple_files(self):
        res = Ledger(
            filepath=[FILEPATH, FILEPATH2],
            command="reg",
            accounts=["Food","House"]
        ).call()
        self.assertListEqual(res, [
            ["date", "payee", "commodity", "quantity", "note"],
            ["2021/08/14","Grocery","JPY","100"," 人参"],
            ["2021/08/13","Grocery","JPY","300"," もも"],
            ["2021/08/14","Daiso","JPY","100"," Sponge"]
        ])

class LedgerReportTest(unittest.TestCase):
    def test_assert_balance(self):
        res = Ledger(
            filepath=FILEPATH,
            command="bal",
            accounts="Liabilities:Card:202109"
        ).call()
        self.assertTrue(reporter.assert_balance(res, -400))
