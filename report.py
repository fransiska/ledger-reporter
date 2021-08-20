#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from ledgerreporter.ledger import Ledger
import ledgerreporter.reporter as reporter

def get_filepaths(folder, year, month, with_monthly_file=True):
    return os.path.join(folder, "{year}/{year}{month}{monthly}.ledger".format(year=year,month=month,monthly="_monthly" if with_monthly_file else ""))

def get_total_budget(filepath):
    res = Ledger(
        filepath=filepath,
        command="bal",
        accounts="^Budget:Control:Yarikuri",
        filter_by="payee",
        filter_args="Budget"
    ).call()
    return reporter.get_balance(res)

def get_total_yarikuri_expenses(filepath):
    res = Ledger(
        filepath=filepath,
        command="bal",
        accounts=["Food","Control:House"]
    ).call()
    return reporter.get_balance(res)

def get_total_yarikuri_paid(filepath):
    res = Ledger(
        filepath=filepath,
        command="bal",
        accounts="^Budget:Control:Yarikuri",
        filter_by="not payee",
        filter_args="Budget"
    ).call()
    return reporter.get_balance(res)

def get_total_yarikuri_remaining(filepath):
    res = Ledger(
        filepath=filepath,
        command="bal",
        accounts="^Budget:Control:Yarikuri"
    ).call()
    return reporter.get_balance(res)

def get_yarikuri_paying_method(filepath):
    return Ledger(
        filepath=filepath,
        command="bal",
        accounts=["Food","Control:House"],
        options=["-w","-r","--flat"]
    ).call()

def get_pay_point(filepath):
    return Ledger(
        filepath=filepath,
        command="reg",
        accounts="^Budget:Point",
        filter_by="amount",
        filter_args="< 0"
    ).call()

def get_charge_by_point(filepath):
    return Ledger(
        filepath=filepath,
        command="reg",
        accounts="^Budget:Point",
        filter_by="amount",
        filter_args="> 0"
    ).call()

def get_pay_not_point(filepath):
    return Ledger(
        filepath=filepath,
        command="bal",
        accounts="Liabilities.*Pay",
        filter_by="amount",
        filter_args="< 0"
    ).call()

def check_monthly_yarikuri(folder, year, month):
    filepath = [
        get_filepaths(folder, year, month),
        get_filepaths(folder, year, month, with_monthly_file=False)]
    next_month = ("0"+str(int(month)+1))[-2:]

    total_yarikuri_expenses = get_total_yarikuri_expenses(filepath)
    print("  Total yarikuri expenses: {}".format(total_yarikuri_expenses))

    res = get_yarikuri_paying_method(filepath)[1:-1]
    total_points = 0
    for r in list(res):
        if any(s in r[0] for s in ["Income:Point","Income:Coupon"]):
            total_points += float(r[2])
            res.remove(r)
    print("    -point ", total_points)

    pay_point = get_pay_point(filepath)
    reg_quantity_i = reporter.get_header_index(pay_point[0], "quantity")
    reg_account_i = reporter.get_header_index(pay_point[0], "account")
    pay_point = [r for r in pay_point if "Apple" not in r[reg_account_i]]
    total_pay_point = sum([float(r[reg_quantity_i]) for r in pay_point[1:]])
    print("    -pay point", total_pay_point)

    total_yarikuri_paid = get_total_yarikuri_paid(filepath)
    point_usage_check = float(total_yarikuri_expenses) + float(total_points) + float(total_pay_point) + float(total_yarikuri_paid)
    print("  Total yarikuri paid: {} {}".format(total_yarikuri_paid, "OK" if abs(point_usage_check) < 1 else "NG {}".format(point_usage_check)))


    total_card_fransiska = 0
    for r in list(res):
        if "Fransiska" in r[0] and "{}{}".format(year,next_month) in r[0]:
            total_card_fransiska += float(r[2])
            res.remove(r)
    print("    -card Fransiska", total_card_fransiska)

    total_cash = 0
    for r in list(res):
        if "Cash" in r[0]:
            total_cash += float(r[2])
            res.remove(r)
    print("    -cash", total_cash)

    total_prepaid = 0
    for r in list(res):
        if any(s in r[0] for s in ["Waon","Mandai"]):
            total_prepaid += float(r[2])
            res.remove(r)
    prepaid_point = sum([float(r[reg_quantity_i]) for r in pay_point[1:] if any(s in r[reg_account_i] for s in ["Waon","Mandai"])])
    total_prepaid -= prepaid_point
    print("    -prepaid", total_prepaid)

    try:
        total_others = sum([float(r[2]) for r in res])
    except IndexError: total_others = 0
    others_point = sum([float(r[reg_quantity_i]) for r in pay_point[1:] if not any(s in r[reg_account_i] for s in ["Waon","Mandai"])])
    total_others -= others_point
    print("    -others", total_others)
   
    paid_source_check = float(total_yarikuri_paid) - float(total_card_fransiska) - float(total_cash) - float(total_prepaid) - total_others
    print("  -------- paid source", "OK" if abs(paid_source_check) < 1 else "NG {}".format(paid_source_check))

    budget = get_total_budget(filepath)
    print("  Total budget: {}".format(budget))

    total_yarikuri_remaining = get_total_yarikuri_remaining(filepath)
    budget_remaining_check = float(budget) + float(total_yarikuri_paid) - float(total_yarikuri_remaining)
    print("  Total remaining {} {}".format(total_yarikuri_remaining, "OK" if abs(budget_remaining_check) < 1 else "NG {}".format(budget_remaining_check)))

def main(folder):
    year = "2021"
    for month in ["01","02","03","04","05","06","07","08"][3:4]:
        print("---")
        print("{}/{}".format(year,month))
        check_monthly_yarikuri(folder, year, month)

if __name__ == "__main__":
    main(sys.argv[1])
