#!/usr/bin/python3
# -*- coding: utf-8 -*-

def get_header_index(row, column):
    try: return row.index(column)
    except IndexError: return len(row)-1

def get_balance(result):
    return result[-1][get_header_index(result[0], "quantity")]

def assert_balance(result, value):
    balance = get_balance(result)
    res = balance == str(value)
    if res:
        return res
    else:
        raise Exception("Balance is {}".format(balance))
