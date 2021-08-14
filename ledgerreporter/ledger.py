#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import csv

class Ledger:
    _bin = ["ledger"]
    _options = ["-w"]

    def __init__(self, filepath, command="reg", print_format=None, filter_by=None, filter_args=None, accounts=""):
        self._command = command
        self._filepath = ["-f", filepath]
        self._print_format = print_format
        self._filter_by = filter_by
        self._filter_args = filter_args
        self._accounts = accounts

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
            return ["date","payee","commodity","quantity","note"]

    @staticmethod
    def generate_filter(filter_by, filter_args):
        if filter_by == "amount":
            if not filter_args.startswith(("<",">","=")):
                filter_args = "== " + filter_args
            return ["expr", '"amount {}"'.format(filter_args)]
        elif filter_by == "payee":
            return ["payee", filter_args]
        elif filter_by == "comment":
            return ["expr", "comment=~/{}/".format(filter_args)]
        else:
            return []

    @staticmethod
    def generate_query(filter_expr, accounts):
        if filter_expr and accounts:
            return filter_expr + ["and {}".format(accounts)]
        else:
            return filter_expr or [accounts]

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
