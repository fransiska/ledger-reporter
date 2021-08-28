#!/usr/bin/python3
# -*- coding: utf-8 -*-

def sum_amounts(res):
    return sum([float(r["quantity"]) for r in res])

def sum_amounts_for_accounts(res, accounts):
    return sum([float(r["quantity"]) for r in res if any(s in r["account"] for s in accounts)])

def remove_accounts(res, accounts):
    for r in list(res):
        if any(s in r["account"] for s in accounts):
            res.remove(r)
