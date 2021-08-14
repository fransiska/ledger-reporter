#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

class Ledger:
    _bin = ["ledger"]
    _options = ["-w"]

    def __init__(self, filepath, command="reg", print_format=None, filter_by=None, filter_args=None, accounts=""):
        self._command = [command]
        self._filepath = ["-f", filepath]
        self._print_format = [self.get_format_keyword(command), print_format if print_format else self.get_default_format(command)]
        self._filter_by = filter_by
        self._filter_args = filter_args
        self._accounts = [accounts] if accounts else []

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
            return "%(account) %(total)\n"
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
            return "%(date) %(payee) %(amount) %(note)\\n"

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
            return filter_expr + ["and"] + accounts
        else:
            return filter_expr or accounts

    def generate_command(self):
        return self._bin + \
            self._command + self._options + \
            self.generate_query(self.generate_filter(self._filter_by, self._filter_args), self._accounts) + \
            self._print_format + self._filepath

    def call(self, encoding="utf8"):
        res = subprocess.run(self.generate_command(), capture_output=True, encoding=encoding)
        return res.stdout
