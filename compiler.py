#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, time, argparse

cmdparser = argparse.ArgumentParser()
cmdparser.add_argument('-c', action='store_true', dest='is_compiler', default=False)
cmdparser.add_argument('-o', dest='output', required=True)
cmdparser.add_argument('--private-dir', dest='private_dir')
cmdparser.add_argument('input', nargs='+')

class Durations:
    def __init__(self):
        self.default_compile = 5
        self.default_link = 1
        self.stdlib_compile = 3
        self.cached_compile = 1

class Compiler:
    def __init__(self, options):
        self.options = options
        self.times = Durations()

    def is_compile(self):
        return self.options.is_compiler

    def run(self):
        if self.is_compile():
            self.compile()
        else:
            self.link()

    def compile(self):
        time.sleep(self.times.default_compile)
        open(self.options.output, 'wb').close()

    def link(self):
        time.sleep(self.times.default_link)
        open(self.options.output, 'wb').close()

if __name__ == '__main__':
    args = cmdparser.parse_args()
    compiler = Compiler(args)
    compiler.run()

