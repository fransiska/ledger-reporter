#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from ledgerreporter.ledger import LedgerOptions, register, balance
from ledgerreporter.reporter import sum_amounts, sum_amounts_for_accounts, remove_accounts

def get_filepaths(folder, year, month, with_monthly_file=False):
    return os.path.join(folder, "{year}/{year}{month}{monthly}.ledger".format(year=year,month=month,monthly="_monthly" if with_monthly_file else ""))

def get_yarikuri_expenses(filepath):
    return balance(LedgerOptions(files=filepath, accounts=["Food","Control:House"]))

def get_yarikuri_paying_method(filepath):
    return balance(LedgerOptions(files=filepath, accounts=["Food","Control:House"], reverse=True))

def get_pay_paid_with_point(filepath):
    return register(LedgerOptions(files=filepath, accounts=["^Budget:Point"], amount="< JPY 0"))

def get_used_yarikuri_budget(filepath):
    return balance(LedgerOptions(files=filepath, accounts=["^Budget:Control:Yarikuri"], payee="not Budget"))

def get_unused_yarikuri_budget(filepath):
    return balance(LedgerOptions(files=filepath, accounts=["^Budget:Control:Yarikuri"]))

def get_total_budget(filepath):
    return balance(LedgerOptions(files=filepath, accounts=["^Budget:Control:Yarikuri"], payee="Budget"))

def check_monthly_yarikuri(folder, year, month):
    filepath = [
        get_filepaths(folder, year, month, with_monthly_file=True),
        get_filepaths(folder, year, month)]
    next_month = ("0"+str(int(month)+1))[-2:]
    yarikuri_expenses = get_yarikuri_expenses(filepath)
    total_yarikuri_expenses = sum_amounts(yarikuri_expenses)
    print("  Total yarikuri expenses: {}".format(total_yarikuri_expenses))

    yarikuri_paying_method = get_yarikuri_paying_method(filepath)
    point_accounts = ["Income:Point","Income:Coupon"]
    total_points = sum_amounts_for_accounts(yarikuri_paying_method, point_accounts)
    remove_accounts(yarikuri_paying_method, point_accounts)
    print("    -point ", total_points)

    pay_paid_with_point = get_pay_paid_with_point(filepath)
    remove_accounts(pay_paid_with_point, ["Apple"])
    total_pay_point = sum_amounts(pay_paid_with_point)
    print("    -pay point", total_pay_point)

    total_used_yarikuri_budget = sum_amounts(get_used_yarikuri_budget(filepath))
    point_usage_check = float(total_yarikuri_expenses) + float(total_points) + float(total_pay_point) + float(total_used_yarikuri_budget)
    print("  Total used yarikuri budget: {} {}".format(total_used_yarikuri_budget, "OK" if abs(point_usage_check) < 1 else "NG {}".format(point_usage_check)))

    cards = ["Line","Yahoo","Rakuten","Pitapa"]
    card_fransiska_accounts = ["Fransiska:{}:{}{}".format(card, year, next_month) for card in cards]
    total_card_fransiska = sum_amounts_for_accounts(yarikuri_paying_method, card_fransiska_accounts)
    remove_accounts(yarikuri_paying_method, card_fransiska_accounts)
    print("    -card Fransiska ", total_card_fransiska)

    cash_accounts = ["Cash"]
    total_cash = sum_amounts_for_accounts(yarikuri_paying_method, cash_accounts)
    remove_accounts(yarikuri_paying_method, cash_accounts)
    print("    -cash ", total_cash)

    prepaid_accounts = ["Waon","Mandai"]
    total_prepaid = sum_amounts_for_accounts(yarikuri_paying_method, prepaid_accounts)
    remove_accounts(yarikuri_paying_method, prepaid_accounts)
    print("    -prepaid ", total_prepaid)

    total_others = sum_amounts(yarikuri_paying_method)
    print("    -others ", total_others)

    paid_source_check = float(total_used_yarikuri_budget) - float(total_card_fransiska) - float(total_cash) - float(total_prepaid) - total_others + total_pay_point
    print("  -------- paid source", "OK" if abs(paid_source_check) < 1 else "NG {}".format(paid_source_check))

    budget = sum_amounts(get_total_budget(filepath))
    print("  Total budget: {}".format(budget))

    total_unused_yarikuri_budget = sum_amounts(get_unused_yarikuri_budget(filepath))
    budget_remaining_check = float(budget) + float(total_used_yarikuri_budget) - float(total_unused_yarikuri_budget)
    print("  Total remaining {} {}".format(total_unused_yarikuri_budget, "OK" if abs(budget_remaining_check) < 1 else "NG {}".format(budget_remaining_check)))

def main(folder):
    year = "2021"
    for month in ["01","02","03","04","05","06","07","08"]:
        print("---")
        print("{}/{}".format(year,month))
        check_monthly_yarikuri(folder, year, month)

if __name__ == "__main__":
    main(sys.argv[1])
