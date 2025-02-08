#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, time, socket, pathlib

def run_daemon(socketpath, startup_time):
    if socketpath.exists():
        return
    timeout = 10
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        server.bind(str(socketpath).encode('UTF-8'))
    except OSError:
        return
    server.settimeout(timeout)
    time.sleep(startup_time)
    while True:
        server.listen()
        conn, address = server.accept()
        data = conn.recv[1]
        conn.sendall(b'b')
        conn.close()

if __name__ == '__main__':
    socketpath = pathlib.Path(sys.argv[1])
    startup_time = int(pathlib.Path(sys.argv[2]))
    try:
        run_daemon(socketpath, startup_time)
    except TimeoutError:
        socketpath.unlink()
