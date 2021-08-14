#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import csv

class Ledger:
    _bin = ["ledger"]

    def __init__(self, filepath, command="reg", options=["-w"], print_format=None, filter_by=None, filter_args=None, accounts=""):
        self._command = command
        self._options = options
        self._filepath = self.parse_filepath(filepath)
        self._print_format = print_format
        self._filter_by = filter_by
        self._filter_args = filter_args
        self._accounts = self.parse_accounts(accounts)

    @staticmethod
    def parse_accounts(accounts):
        if isinstance(accounts, list):
            return accounts
        elif accounts:
            return [accounts]
        else:
            return []

    @staticmethod
    def parse_filepath(filepath):
        if isinstance(filepath, list):
            array = []
            for f in filepath:
                array += ["-f", f]
            return array
        else:
            return ["-f", filepath]

    @staticmethod
    def get_format_keyword(command):
        if command == "bal":
            return "--balance-format"
        elif command == "csv":
            return "--csv-format"
        else:
            return "--format"

    @staticmethod
    def get_default_format(command):
        if command == "bal":
            return "%(quoted(account))," \
                "%(quoted(commodity(scrub(display_total))))," \
                "%(quoted(quantity(scrub(display_total))))\n"
        elif command == "csv":
            return "%(quoted(date))," \
                "%(quoted(code))," \
                "%(quoted(payee))," \
                "%(quoted(display_account))," \
                "%(quoted(commodity(scrub(display_amount))))," \
                "%(quoted(quantity(scrub(display_amount))))," \
                "%(quoted(cleared ? \"*\" : (pending ? \"!\" : \"\")))," \
                "%(quoted(join(note | xact.note)))\n"
        else:
            return "%(quoted(date)),%(quoted(payee)),"\
                "%(quoted(display_account))," \
                "%(quoted(commodity(scrub(display_amount))))," \
                "%(quoted(quantity(scrub(display_amount))))," \
                "%(quoted(note))\n"

    @classmethod
    def generate_print_format(cls, command, print_format):
        return [cls.get_format_keyword(command), print_format if print_format else cls.get_default_format(command)]

    @staticmethod
    def get_default_header(command):
        if command == "bal":
            return ["account","commodity","quantity"]
        elif command == "csv":
            return ["date","code","payee","account","commodity","quantity","cleared","note"]
        else:
            return ["date","payee","account","commodity","quantity","note"]

    @staticmethod
    def generate_filter(filter_by, filter_args):
        if not filter_by:
            return []

        if filter_by == "amount":
            if not filter_args.startswith(("<",">","=")):
                filter_args = "== " + filter_args
            return ["expr", 'amount {}'.format(filter_args)]
        elif "payee" in filter_by:
            return filter_by.split(" ") + [filter_args]
        elif filter_by == "comment":
            return ["expr", "comment=~/{}/".format(filter_args)]
        else:
            raise Exeption("Filter not supported")

    @staticmethod
    def generate_query(filter_expr, accounts):
        if filter_expr and accounts:
            return filter_expr + ["and", accounts[0]]
        elif accounts:
            return accounts
        else:
            return filter_expr or []

    def generate_command(self):
        return self._bin + \
            [self._command] + self._options + \
            self.generate_query(self.generate_filter(self._filter_by, self._filter_args), self._accounts) + \
            self.generate_print_format(self._command, self._print_format) + \
            self._filepath

    def call(self, encoding="utf8"):
        res = subprocess.run(self.generate_command(), capture_output=True, encoding=encoding)
        data = list(csv.reader(res.stdout.splitlines()))
        if not self._print_format:
            data.insert(0, self.get_default_header(self._command))
        return data
