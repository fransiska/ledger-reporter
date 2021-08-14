#!/usr/bin/python3
# -*- coding: utf-8 -*-

def get_header_index(row, column):
    try: return row.index(column)
    except IndexError: return len(row)-1

def assert_balance(result, value):
    return result[-1][get_header_index(result[0], "quantity")] == str(value)
