#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from ledgerreporter.ledger import LedgerOptions, balance, register

def main(filepath):
    ledgers = [
        balance(LedgerOptions(files=filepath, accounts=["Expenses"])),
        register(LedgerOptions(files=filepath, accounts=["Expenses"])),
        register(LedgerOptions(files=filepath, accounts=["Expenses"], amount="== JPY 100")),
        register(LedgerOptions(files=filepath, accounts=["Food", "House"])),
    ]
    for ledger in ledgers:
        print("---")
        [print(l) for l in ledger]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("Usage: python ledger.py <ledger_file> <ledger_file2>")
