#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import csv

from dataclasses import dataclass, field

@dataclass
class LedgerOptions:
    files: list = field(default_factory=list)
    accounts: list = field(default_factory=list)
    payee: str = ""
    amount: str = ""
    reverse: bool = False
    flat: bool = True

    @staticmethod
    def parse_files(files):
        if isinstance(files, list):
            array = []
            for f in files:
                array += ["-f", f]
            return array
        else:
            return ["-f", filepath]

    @staticmethod
    def parse_accounts(accounts):
        if isinstance(accounts, list):
            return accounts
        elif accounts:
            return [accounts]
        else:
            return []

    @staticmethod
    def parse_payee(payee):
        if payee.startswith("not "):
            return ["not", "payee", payee[4:]]
        elif payee:
            return ["payee", payee]
        else:
            return []

    @staticmethod
    def parse_amount(amount):
        return ["expr", 'amount {}'.format(amount)] if amount else []

    @staticmethod
    def parse_reverse(reverse):
        return ["-r"] if reverse else []

    @staticmethod
    def parse_flat(flat):
        return ["--flat"] if flat else []

    def parse_conditions(self):
        accounts = self.parse_accounts(self.accounts)
        payee = self.parse_payee(self.payee)
        amount = self.parse_amount(self.amount)
        conditions = accounts
        if len(payee):
            if len(conditions):
                conditions  += ["and"]
            conditions += payee
        if len(amount):
            if len(conditions):
                conditions  += ["and"]
            conditions += amount
        return conditions

    def to_command(self):
        return self.parse_files(self.files) + \
            self.parse_reverse(self.reverse) + \
            self.parse_flat(self.flat) + \
            self.parse_conditions()

def balance(options: LedgerOptions, encoding="utf8"):
    res = call_ledger("bal", options, encoding)
    return parse_result(get_result_header("bal"), res)

def register(options: LedgerOptions, encoding="utf8"):
    res = call_ledger("reg", options, encoding)
    return parse_result(get_result_header("reg"), res)

def get_print_format(command):
    if command not in ["bal","reg"]: return []
    return {
        "bal": ["--balance-format", "%(quoted(account))," \
                "%(quoted(commodity(scrub(display_total))))," \
                "%(quoted(quantity(scrub(display_total))))\n"],
        "reg": ["--format", "%(quoted(date)),%(quoted(payee)),"\
                "%(quoted(display_account))," \
                "%(quoted(commodity(scrub(display_amount))))," \
                "%(quoted(quantity(scrub(display_amount))))," \
                "%(quoted(note))\n"]
        }[command]

def get_result_header(command):
    if command not in ["bal","reg"]: return []
    return {
        "bal": ("account","commodity","quantity"),
        "reg": ("date","payee","account","commodity","quantity","note")
    }[command]

def parse_result(header, res):
    return [dict(l) for l in csv.DictReader(res.stdout.splitlines(), fieldnames=header) if l["account"]]

def call_ledger(command, options: LedgerOptions, encoding="utf8"):
    return subprocess.run(
        ["ledger", command] + options.to_command() + get_print_format(command), \
        capture_output=True, encoding=encoding)
