#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from ledgerreporter.ledger import Ledger
import ledgerreporter.reporter as reporter

def check_monthly_one_account(folder, year, month, account, with_monthly_file=True):
    filepath = [os.path.join(folder, "{year}/{year}{month}.ledger".format(year=year,month=month))]
    if with_monthly_file:
        filepath.append(os.path.join(folder, "{year}/{year}{month}_monthly.ledger".format(year=year,month=month)))
    return Ledger(
        filepath=filepath,
        command="bal",
        accounts=account
    ).call()

def check_monthly_yarikuri(folder, year, month):
    for account in ["Food","House",["Food","House"]]:
        res = check_monthly_one_account(folder, year, month, account)
        print("  {account} is {bal}".format(account=account, bal=reporter.get_balance(res)))

    m = ("0"+str(int(month)+1))[-2:]
    account = "'Liabilities.*2021{}'".format(m)
    res = check_monthly_one_account(folder, year, month, account, with_monthly_file=False)
    print("  {account} is {bal}".format(account=account, bal=reporter.get_balance(res)))

def main(folder):
    year = "2021"
    for month in ["06","07"]:
        print("---")
        print("{}/{}".format(year,month))
        check_monthly_yarikuri(folder, year, month)

if __name__ == "__main__":
    main(sys.argv[1])
