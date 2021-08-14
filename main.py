#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from ledgerreporter.ledger import Ledger

def main(filepath):
    ledger = Ledger(
        filepath=filepath,
        command="bal",
        accounts="Expenses"
    )
    res = ledger.call()
    print(res)

    ledger = Ledger(
        filepath=filepath,
        filter_by="amount",
        filter_args="JPY 100"
    )
    res = ledger.call()
    print(res)

    ledger = Ledger(
        filepath=filepath,
        command="csv",
        accounts="Expenses"
    )
    res = ledger.call()
    for l in csv.reader(res):
        print(l)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python ledger.py <ledger_file>")
