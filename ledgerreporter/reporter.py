#!/usr/bin/python3
# -*- coding: utf-8 -*-

def get_header_index(row, column):
    try: return row.index(column)
    except IndexError: return len(row)-1

def get_balance(balance_result):
    if len(balance_result) < 2:
        raise Exception("No balance")
    return balance_result[-1][get_header_index(balance_result[0], "quantity")]

def assert_balance(balance_result, value):
    balance = get_balance(balance_result)
    res = balance == str(value)
    if res:
        return res
    else:
        raise Exception("Balance is {}".format(balance))
