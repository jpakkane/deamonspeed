#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, time, argparse, socket

cmdparser = argparse.ArgumentParser()
cmdparser.add_argument('-c', action='store_true', dest='is_compiler', default=False)
cmdparser.add_argument('-o', dest='output', required=True)
cmdparser.add_argument('--private-dir', dest='private_dir', default=None)
cmdparser.add_argument('input', nargs='+')

class Durations:
    def __init__(self):
        self.default_compile = 5
        self.default_link = 1
        self.stdlib_compile = 3
        self.daemon_compile = 1

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
        if self.options.private_dir is not None:
            self.compile_with_daemon()
        else:
            time.sleep(self.times.default_compile)
            open(self.options.output, 'wb').close()

    def compile_with_daemon(self):
        socket_path = pathlib.Path(self.options.private_dir) / 'daemonsocket'
        os.subprocess.Popen(['../daemon.py', socket_path, f'{self.times.stdlib_compile}'])
        self.connect_daemon(socket_path)
        time.sleep(self.times.daemon_compile)

    def connect_daemon(self, socket_path):
        socket_path_bytes = str(socket_path).encode('UTF-8')
        for i in range(10):
            time.sleep(1)
            conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            conn.connect(socket_path)
            conn.sendall(b'a')
            response = conn.recv(1)
            conn.close()
            return
        sys.exit('Could not connect to compiler daemon.')

    def link(self):
        time.sleep(self.times.default_link)
        open(self.options.output, 'wb').close()

if __name__ == '__main__':
    args = cmdparser.parse_args()
    compiler = Compiler(args)
    compiler.run()

