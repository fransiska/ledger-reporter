#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from ledgerreporter.ledger import Ledger

def main(filepath):
    ledgers = [
        Ledger(
            filepath=filepath,
            command="bal",
            accounts="Expenses"
        ),
        Ledger(
            filepath=filepath,
            filter_by="amount",
            filter_args="JPY 100"
        ),
        Ledger(
            filepath=filepath,
            command="csv",
            accounts="Expenses"
        )]
    for ledger in ledgers:
        print("*",ledger._command[0])
        res = ledger.call()
        for l in res:
            print(l)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python ledger.py <ledger_file>")
