#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from ledgerreporter.ledger import Ledger

def main(filepath):
    ledger = Ledger(
        filepath=filepath,
        filter_by="amount",
        filter_args="JPY 100"
    )
    res = ledger.call()
    print(res)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python ledger.py <ledger_file>")
