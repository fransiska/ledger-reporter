#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

class Ledger:
    _bin = ["ledger"]
    _options = ["-w"]

    def __init__(self, filepath, command="reg", print_format=["--format","%(date) %(payee) %(amount) %(note)\\n"], filter_by=None, filter_args=None):
        self._command = [command]
        self._filepath = ["-f", filepath]
        self._print_format = print_format
        self._filter_by = filter_by
        self._filter_args = filter_args

    @staticmethod
    def generate_filter(filter_by, filter_args):
        if filter_by == "amount":
            return ["expr", '"amount == {}"'.format(filter_args)]
        elif filter_by == "payee":
            return ["payee", filter_args]
        elif filter_by == "comment":
            return ["expr", "comment=~/{}/".format(filter_args)]
        else:
            return []

    def generate_command(self):
        return self._bin + self._command + self.generate_filter(self._filter_by, self._filter_args) + self._options + self._print_format + self._filepath

    def call(self, encoding="utf8"):
        res = subprocess.run(self.generate_command(), capture_output=True, encoding=encoding)
        return res.stdout.splitlines()
